'''
PassportEye::MRZ: Machine-readable zone extraction and parsing.
Command-line scripts

Author: Konstantin Tretyakov
License: MIT
'''
import argparse
import glob
import json
import logging
import multiprocessing
import os
import shutil
import sys
import time
from collections import Counter
import pkg_resources
from skimage import io
import numpy as np
from pytesseract.pytesseract import TesseractNotFoundError, TesseractError
import passporteye
from .image import read_mrz, MRZPipeline


def process_file(params):
    """
    Processes a file and returns the parsed MRZ (or None if no candidate regions were even found).

    The input argument is a list (filename, save_roi, extra_params).
    (Because we need to use this function within imap_unordered)
    """
    tic = time.time()
    filename, save_roi, extra_params = params
    result = read_mrz(filename, save_roi=save_roi, extra_cmdline_params=extra_params)
    walltime = time.time() - tic
    return (filename, result, walltime)


def evaluate_mrz():
    """
    A script for evaluating the current MRZ recognition pipeline by applying it to a list of files in a directory and reporting how well it went.
    """
    parser = argparse.ArgumentParser(description='Run the MRZ OCR recognition algorithm on the sample test data, reporting the quality summary.')
    parser.add_argument('-j', '--jobs', default=1, type=int, help='Number of parallel jobs to run')
    parser.add_argument('-dd', '--data-dir', default=pkg_resources.resource_filename('passporteye.mrz', 'testdata'),
                        help='Read files from this directory instead of the package test files')
    parser.add_argument('-sd', '--success-dir', default=None,
                        help='Copy files with successful (nonzero score) extraction results to this directory')
    parser.add_argument('-fd', '--fail-dir', default=None,
                        help='Copy files with unsuccessful (zero score) extraction resutls to this directory')
    parser.add_argument('-rd', '--roi-dir', default=None,
                        help='Extract ROIs to this directory')
    parser.add_argument('-l', '--limit', default=-1, type=int, help='Only process the first <limit> files in the directory.')
    parser.add_argument('--legacy', action='store_true',
                        help='Use the "legacy" Tesseract OCR engine (--oem 0). Despite the name, it most often results in better '
                        'results. It is not the default option, because it will only work if '
                        'your Tesseract installation includes the legacy *.traineddata files. You can download them at '
                        'https://github.com/tesseract-ocr/tesseract/wiki/Data-Files#data-files-for-version-400-november-29-2016')
    args = parser.parse_args()
    files = sorted(glob.glob(os.path.join(args.data_dir, '*.*')))
    if args.limit >= 0:
        files = files[0:args.limit]

    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger("evaluate_mrz")

    tic = time.time()
    pool = multiprocessing.Pool(args.jobs)
    log.info("Preparing computation for %d files from %s", len(files), args.data_dir)
    log.info("Running %d workers", args.jobs)
    results = []
    save_roi = args.roi_dir is not None
    for d in [args.success_dir, args.fail_dir, args.roi_dir]:
        if d is not None and not os.path.isdir(d):
            os.mkdir(d)

    def valid_score(mrz_):
        return 0 if mrz_ is None else mrz_.valid_score

    def score_change_type(filename, mrz_):
        try:
            new_score = valid_score(mrz_)
            old_score = int(os.path.basename(filename).split('_')[0])
            schange = new_score - old_score
            return '=' if schange == 0 else ('>' if schange > 0 else '<')
        except Exception:
            return '?'

    method_stats = Counter()

    extra_params = '--oem 0' if args.legacy else ''
    for result in pool.imap_unordered(process_file, [(f, save_roi, extra_params) for f in files]):
        filename, mrz_, walltime = result
        results.append(result)
        log.info("Processed %s in %0.2fs (score %d) [%s]", os.path.basename(filename), walltime, valid_score(mrz_), score_change_type(filename, mrz_))
        log.debug("\t%s", mrz_)

        vs = valid_score(mrz_)
        if args.success_dir is not None and vs > 0:
            shutil.copyfile(filename, os.path.join(args.success_dir, '%d_%s' % (vs, os.path.basename(filename))))
        if args.fail_dir is not None and vs == 0:
            shutil.copyfile(filename, os.path.join(args.fail_dir, '%d_%s' % (vs, os.path.basename(filename))))
        if args.roi_dir is not None and mrz_ is not None and 'roi' in mrz_.aux:
            roi_fn = '%d_roi_%s.png' % (vs, os.path.basename(filename))
            io.imsave(os.path.join(args.roi_dir, roi_fn), mrz_.aux['roi'])

        if vs > 0 and 'method' in mrz_.aux:
            method_stats[mrz_.aux['method']] += 1

    num_files = len(results)
    score_changes = [score_change_type(fn, mrz_) for fn, mrz_, wt in results]
    scores = [valid_score(mrz_) for fn, mrz_, wt in results]
    num_perfect = scores.count(100)
    num_invalid = scores.count(0)
    total_score = sum(scores)
    total_computation_walltime = sum([wt for fn, mrz_, wt in results])
    total_walltime = time.time() - tic
    log.info("Completed")
    print("Walltime:          %0.2fs" % total_walltime)
    print("Compute walltime:  %0.2fs" % total_computation_walltime)
    print("Processed files:   %d" % num_files)
    print("Perfect parses:    %d" % num_perfect)
    print("Invalid parses:    %d" % num_invalid)
    print("Improved parses:   %d" % len([x for x in score_changes if x == '>']))
    print("Worsened parses:   %d" % len([x for x in score_changes if x == '<']))
    print("Total score:       %d" % total_score)
    print("Mean score:        %0.2f" % (float(total_score)/num_files))
    print("Mean compute time: %0.2fs" % (total_computation_walltime/num_files))
    print("Methods used:")
    for stat in method_stats.most_common():
        print("  %s: %d" % stat)


def mrz():
    """
    Command-line script for extracting MRZ from a given image
    """
    parser = argparse.ArgumentParser(description='Run the MRZ OCR recognition algorithm on the given image.')
    parser.add_argument('filename')
    parser.add_argument('--json', action='store_true', help='Produce JSON (rather than tabular) output')
    parser.add_argument('--legacy', action='store_true',
                        help='Use the "legacy" Tesseract OCR engine (--oem 0). Despite the name, it most often results in better '
                        'results. It is not the default option, because it will only work if '
                        'your Tesseract installation includes the legacy *.traineddata files. You can download them at '
                        'https://github.com/tesseract-ocr/tesseract/wiki/Data-Files#data-files-for-version-400-november-29-2016')
    parser.add_argument('-r', '--save-roi', default=None,
                        help='Output the region of the image that is detected to contain the MRZ to the given png file.')
    parser.add_argument('--version', action='version', version='PassportEye MRZ v%s' % passporteye.__version__)
    args = parser.parse_args()

    try:
        extra_params = '--oem 0' if args.legacy else ''
        filename, mrz_, walltime = process_file((args.filename, args.save_roi is not None, extra_params))
    except TesseractNotFoundError:
        sys.stderr.write("ERROR: The tesseract executable was not found.\n"
                         "Please, make sure Tesseract is installed and the appropriate directory is included "
                         "in your PATH environment variable.\n")
        sys.exit(1)
    except TesseractError as ex:
        sys.stderr.write("ERROR: %s" % ex.message)
        sys.exit(ex.status)
    
    d = mrz_.to_dict() if mrz_ is not None else {'mrz_type': None, 'valid': False, 'valid_score': 0}
    d['walltime'] = walltime
    d['filename'] = filename

    if args.save_roi is not None and mrz_ is not None and 'roi' in mrz_.aux:
        io.imsave(args.save_roi, (mrz_.aux['roi'] * 255).astype(np.uint8))

    if not args.json:
        for k in d:
            print("%s\t%s" % (k, str(d[k]).replace('\n', ' ')))
    else:
        print(json.dumps(d, indent=2))


def extract_mrz_rois():
    """
    Command-line script for extracting all potential MRZ regions from a given image as images
    """
    parser = argparse.ArgumentParser(description='Extract all potential MRZ regions from a given image and output as individual PNG files.')
    parser.add_argument('filename')
    parser.add_argument('-d', '--output-dir', default='.',
                        help='The directory where the images for the potential MRZ regions will be output (default is the current directory). '
                        'The files created will be named 1.png, 2.png, ...')
    parser.add_argument('-c', '--create-dir', action='store_true', help='Force the creation of the directory (and all parents) if it does not exist.')
    parser.add_argument('--version', action='version', version='PassprtEye extract_mrz_rois v%s' % passporteye.__version__)
    args = parser.parse_args()

    rois = MRZPipeline(args.filename)['rois']
    if args.create_dir:
        os.makedirs(args.output_dir, exist_ok=True)

    for n, img in enumerate(rois, 1):
        io.imsave(os.path.join(args.output_dir, '%d.png' % n), (img * 255).astype(np.uint8))
