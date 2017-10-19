import logging
import os
import sys
from subprocess import check_call


def get_snakefile():
    sf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Snakefile")
    if not os.path.exists(sf):
        sys.exit("Unable to locate the Snakemake workflow file; tried %s" % sf)
    return sf


def annotate(config, jobs, out_dir, no_conda, dryrun, snakemake_args):
    if not os.path.exists(config):
        logging.critical("Config not found: %s" % config)
        sys.exit(1)
    out_dir = os.path.realpath(out_dir)
    cmd = ("snakemake --snakefile {snakefile} --directory {out_dir} "
           "--printshellcmds --jobs {jobs} --rerun-incomplete "
           "--configfile '{config}' --nolock {conda} {dryrun} "
           "--config workflow=annotate {add_args} "
           "{args}").format(snakefile=get_snakefile(),
                            out_dir=out_dir,
                            jobs=jobs,
                            config=config,
                            conda="" if no_conda else "--use-conda",
                            dryrun="--dryrun" if dryrun else "",
                            add_args="" if snakemake_args and snakemake_args[0].startswith("-") else "--",
                            args=" ".join(snakemake_args))
    logging.info("Executing: %s" % cmd)
    check_call(cmd, shell=True)


def assemble(config, jobs, out_dir, no_conda, dryrun, snakemake_args):
    if not os.path.exists(config):
        logging.critical("Config not found: %s" % config)
        sys.exit(1)
    out_dir = os.path.realpath(out_dir)
    cmd = ("snakemake --snakefile {snakefile} --directory {out_dir} "
           "--printshellcmds --jobs {jobs} --rerun-incomplete "
           "--configfile '{config}' --nolock {conda} {dryrun} "
           "--config workflow=complete {add_args} "
           "{args}").format(snakefile=get_snakefile(),
                            out_dir=out_dir,
                            jobs=jobs,
                            config=config,
                            conda="" if no_conda else "--use-conda",
                            dryrun="--dryrun" if dryrun else "",
                            add_args="" if snakemake_args and snakemake_args[0].startswith("-") else "--",
                            args=" ".join(snakemake_args))
    logging.info("Executing: %s" % cmd)
    check_call(cmd, shell=True)


def download(jobs, out_dir, snakemake_args):
    out_dir = os.path.realpath(out_dir)
    cmd = ("snakemake --snakefile {snakefile} --directory {parent_dir} "
           "--printshellcmds --jobs {jobs} --rerun-incomplete "
           "--nolock "
           "--config workflow=download db_dir='{out_dir}' {add_args} "
           "{args}").format(snakefile=get_snakefile(),
                            parent_dir=os.path.dirname(out_dir),
                            jobs=jobs,
                            out_dir=out_dir,
                            add_args="" if snakemake_args and snakemake_args[0].startswith("-") else "--",
                            args=" ".join(snakemake_args))
    logging.info("Executing: %s" % cmd)
    check_call(cmd, shell=True)
