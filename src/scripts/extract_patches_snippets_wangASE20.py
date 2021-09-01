#!/usr/bin/python
import sys, os, subprocess, fnmatch, shutil, csv, re, datetime
import time
import traceback
from os import listdir
from os.path import isfile, join
from pathlib import Path, PureWindowsPath, PurePath
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

sucess_logger = logging.getLogger("success")
error_logger = logging.getLogger("error")

# D4J_CHECKOUT_DIR = 'H:/defects4j_checkout_temp'
D4J_CHECKOUT_DIR = 'H:/defects4j_checkout'

# PATCHES_DATASET_DIR = 'H:/DatasetPatches/Defects4J/rawData/HeYe2019/Patches'
PATCHES_DATASET_DIR = 'H:/DatasetPatches/Defects4J/rawData/WangASE2020/Patches'

# DIFF_SNIPPETS_EXTRACTOR_JAR = 'C:/workplace/staticanalysis/release/patchanalyser-0.0.1-SNAPSHOT-jar-with-dependencies.jar'
DIFF_SNIPPETS_EXTRACTOR_JAR = 'C:/workplace/staticanalysis/target/patchanalyser-0.0.1-SNAPSHOT-jar-with-dependencies.jar'

# OUTPUT_DIR = 'H:/Defects4J_snippets_wangASE20/'
OUTPUT_DIR = 'H:/Defects4J_snippets_wangASE20_final/'
# OUTPUT_DIR = 'H:/Defects4J_snippets_wangASE20_final_patchOriginSource/retry/'

# errorPatchesFiles = os.path.join('H:/Defects4J_snippets_wangASE20_final_patchOriginSource/','errorLog.txt''')

devnullfile = os.path.join(OUTPUT_DIR, "devnullfile.txt")
devnull = open(devnullfile, 'w')


def init_logger(output_dir):
    logfilePath = os.path.join(output_dir, "extract_snippet_log.txt")

    # logging.getLogger().addHandler(logging.StreamHandler())
    # logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logFormatter = logging.Formatter("[%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler(logfilePath)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    errorFileHandler = logging.FileHandler(os.path.join(output_dir, "errorLog.txt"))
    # errorFileHandler.setFormatter(logFormatter)
    error_logger.addHandler(errorFileHandler)
    sucess_logger.addHandler(logging.FileHandler(os.path.join(output_dir, "sucessLog.txt")))


def normalizePath(org_path):
    if os.name == 'nt':
        normalize_path = PureWindowsPath(org_path)
    else:
        normalize_path = PurePath(org_path)
    return str(normalize_path)


def extract_patched_methods_snippets(org_dir, patched_dir, output_dir):
    jar_file = normalizePath(DIFF_SNIPPETS_EXTRACTOR_JAR)
    java_class = 'skku.selab.staticanalysis.DiffSnippetExtractor'
    cmd = 'java -cp "%s" "%s" -s "%s" -p "%s" -o "%s"' % (jar_file, java_class, org_dir, patched_dir, output_dir)
    logger.debug(cmd)
    cmdOutput = subprocess.check_output(cmd, shell=True, stdin=None, stderr=devnull)
    logger.debug(cmdOutput)


def extract_patched_files(patchFile, org_dir, output_dir):
    logger.info("extract_patched_files: %s" % patchFile)
    output_dir=normalizePath(output_dir)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    # copy patch file
    head, tail = os.path.split(patchFile)
    dstPatchFile = normalizePath(os.path.join(output_dir, tail))
    copyFile(patchFile, dstPatchFile)

    with open(patchFile) as f:
        difffiles = f.read().split('\n\n\n')
        for idx,diffs in enumerate(difffiles):
            #first_line = diffs.split('\n')[0]
            first_line = next((line for line in diffs.split('\n') if line.startswith('--- ')),None)
            if first_line is None:
                continue
            # original buggy file patch
            filepath = first_line.split('--- ')[1]
            filepath= filepath.strip()
            original_file = normalizePath(org_dir + filepath)

            head, tail = os.path.split(original_file)
            patchFilepath='diff'+str(idx)+'_'+tail+'.patch'
            # split a patch to several temporary patches in case one patch containes many fixes for different files
            tmppatch = normalizePath(os.path.join(output_dir, patchFilepath))
            tmpfile = open(tmppatch, "w")
            tmpfile.write(diffs)
            tmpfile.close()

            out_origin_filepath = normalizePath(os.path.join(output_dir, 'origin' + filepath))
            out_patched_filepath = normalizePath(os.path.join(output_dir, 'patched' + filepath))

            # copy to origin
            Path(os.path.dirname(out_origin_filepath)).mkdir(parents=True, exist_ok=True)
            cmd = 'cp %s %s' % (original_file, out_origin_filepath)
            logger.debug(cmd)
            cmdOutput = subprocess.check_output(cmd, shell=True, stdin=None, stderr=devnull)
            logger.debug(cmdOutput)

            # copy to patched dir
            Path(os.path.dirname(out_patched_filepath)).mkdir(parents=True, exist_ok=True)
            cmd = 'cp -p %s %s' % (original_file, out_patched_filepath)
            logger.debug(cmd)
            cmdOutput = subprocess.check_output(cmd, shell=True, stdin=None, stderr=devnull)
            logger.debug(cmdOutput)

            # apply patch
            cmd = 'patch -u -l --fuzz=10  -i  %s %s' % (tmppatch, out_patched_filepath)
            logger.debug(cmd)
            cmdOutput = subprocess.check_output(cmd, shell=True, stdin=None, stderr=devnull)
            logger.debug(cmdOutput)
            #os.remove(tmppatch)

    logger.debug("exit apply patch")

def copyFile(src,dst):
    shutil.copyfile(src,dst)


def extract_snippets(patchfile, projectId, bugId, toolId, patchId, output_dir):
    logger.info("extract_snippets(%s,%s,%s,%s,%s,output_dir)" % (patchfile, projectId, bugId, toolId, patchId))
    bugName = projectId + bugId
    patchName = bugName + '_' + toolId + '_' + patchId

    original_checkout_dir = normalizePath(os.path.join(D4J_CHECKOUT_DIR, projectId, bugName))

    output_patched_files_dir = os.path.join(output_dir, 'files', bugName, patchName)
    output_snippets_dir = os.path.join(output_dir, 'snippets', bugName, patchName)

    extract_patched_files(patchfile, original_checkout_dir, output_patched_files_dir)

    org_files_dir = normalizePath(os.path.join(output_patched_files_dir, "origin"))
    patched_files_dir = normalizePath(os.path.join(output_patched_files_dir, "patched"))
    extract_patched_methods_snippets(org_files_dir, patched_files_dir, output_snippets_dir)

def process_file_patch(diff_file,output_root_dir):
    patches_dir = os.path.dirname(diff_file)
    file = os.path.basename(diff_file)
    filename = os.path.splitext(file)[0]
    arraynames = filename.split("-")
    projectId = arraynames[1]
    bugId = arraynames[2]
    toolId = arraynames[3]
    patchId = arraynames[0]
    filepath = os.path.join(patches_dir, file)
    if "Dcorrect" in patches_dir:
        patchId += "_correct"
    elif "Doverfitting" in patches_dir:
        patchId += "_overfitting"
    elif "Ddifferent" in patches_dir:
        patchId += "_correct_different"
    elif "Dsame" in patches_dir:
        patchId += "_correct_same"
    else:
        patchId += "_unknown"
    try:
        extract_snippets(filepath, projectId, bugId, toolId, patchId, output_root_dir)
        bugName = projectId + bugId
        patchName = bugName + '_' + toolId + '_' + patchId
        sucess_logger.info(
            '%s | %s | %s | %s | %s' % (filepath, projectId, bugName, toolId, patchName))
    except Exception as ex:
        tb = traceback.format_exc()
        logger.error("'%s' while processing file: %s\n %s" % (ex, filepath, tb))
        # error_logger.info('%s | %s | %s | %s | %s' % (filepath, projectId, projectId + bugId, toolId, toolId + patchId))
        error_logger.info('%s' % filepath)

def travFolder(patches_dir, output_root_dir):
    listdirs = os.listdir(patches_dir)
    for f in listdirs:
        pattern = 'patch*.patch'
        if os.path.isfile(os.path.join(patches_dir, f)):
            if fnmatch.fnmatch(f, pattern):
                filepath = os.path.join(patches_dir, f)
                process_file_patch(filepath, output_root_dir)
        else:
            if 'tmp.patch' not in f:
                travFolder(patches_dir + '/' + f, output_root_dir)


def travFileLists(patches_file, output_root_dir):
    with open(patches_file) as f:
        lines = [x.strip() for x in f.readlines()]
        for f in lines:
            if os.path.isfile(f):
                process_file_patch(f,output_root_dir)
            else:
                logger.error('patch file not found: "%s"' % f)

if __name__ == '__main__':
    output_dir = OUTPUT_DIR
    patches_dataset_dir = PATCHES_DATASET_DIR

    init_logger(output_dir)
    travFolder(patches_dataset_dir, output_dir)
    # travFileLists(errorPatchesFiles, output_dir)

    # patchFile='H:/DatasetPatches/Defects4J/rawData/HeYe2019/Patches/Doverfitting/Arja/Chart/patch1-Chart-1-Arja-plausible.patch'
    #
    # org_dir = 'H:/temp/Chart1'
    # output_patched_files_dir = 'H:/tmp/files/Chart1'
    # org_files_dir = normalizePath(os.path.join(output_patched_files_dir, "origin"))
    # patched_files_dir = normalizePath(os.path.join(output_patched_files_dir, "patched"))
    #
    # output_snippets_dir = 'H:/tmp/snippets/Chart1'
    #
    # extract_patched_files(patchFile,org_dir,output_patched_files_dir)
    #
    # extract_patched_methods_snippets(org_files_dir,patched_files_dir,output_snippets_dir)
