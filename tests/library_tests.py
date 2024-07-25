from __future__ import annotations
import os

import argparse
from pathlib import Path
from sys import path
import subprocess
import unittest
from typing import Any

from juno_library import Pipeline
from juno_library.helper_functions import (
    error_formatter,
    message_formatter,
    SnakemakeKwargsAction,
    validate_file_has_min_lines,
    get_commit_git,
    get_repo_url,
)

main_script_path = str(Path(__file__).absolute().parent.parent)
path.insert(0, main_script_path)


def make_non_empty_file(
    file_path: str | Path, content: str = "this\nfile\nhas\ncontents"
) -> None:
    with open(file_path, "w") as file_:
        file_.write(content)


default_args: dict[str, Any] = dict(
    pipeline_name="juno_library",
    pipeline_version="v0.0.0",
)
default_argv = ["i", "fake_input", "-o", "fake_output_dir", "--local"]


class TestTextJunoHelpers(unittest.TestCase):
    """Testing Text Helper Functions"""

    def test_error_formatter(self) -> None:
        """Testing that the error formatter does add the color codes to the text"""
        self.assertEqual(error_formatter("message"), "\033[0;31mmessage\n\033[0;0m")

    def test_message_formatter(self) -> None:
        """Testing that the message formatter does add the color codes to the text"""
        self.assertEqual(message_formatter("message"), "\033[0;33mmessage\n\033[0;0m")


class TestFileJunoHelpers(unittest.TestCase):
    """Testing File Helper Functions"""

    def test_validate_file_has_min_lines(self) -> None:
        """Testing that the function to check whether a file is empty works.
        It should return True if nonempty file"""
        nonempty_file = "nonempty.txt"
        make_non_empty_file(nonempty_file)
        self.assertTrue(validate_file_has_min_lines(nonempty_file))
        os.system(f"rm -f {nonempty_file}")

    def test_validate_file_has_min_lines_2(self) -> None:
        """Testing that the function to check whether a file is empty works.
        It should return True if file is empty but no min_num_lines is given
        and False if empty file and a min_num_lines of at least 1"""
        empty_file = "empty.txt"
        open(empty_file, "a").close()
        self.assertFalse(validate_file_has_min_lines(empty_file, min_num_lines=1))
        os.system(f"rm -f {empty_file}")

    def test_validate_is_nonempty_when_gzipped(self) -> None:
        """Testing that the function to check whether a gzipped file is empty
        works. It should return True if file is empty but no min_num_lines is
        given and False if empty file and a min_num_lines of at least 1"""
        empty_file = "empty.txt"
        open(empty_file, "a").close()
        os.system(f"gzip -f {empty_file}")
        self.assertTrue(validate_file_has_min_lines(f"{empty_file}.gz"))
        self.assertFalse(
            validate_file_has_min_lines(f"{empty_file}.gz", min_num_lines=3)
        )
        os.system(f"rm -f {empty_file}")
        os.system(f"rm -f {empty_file}.gz")


class TestJunoHelpers(unittest.TestCase):
    """Testing Helper Functions"""

    @unittest.skipIf(
        not Path("/data/BioGrid/hernanda/").exists(),
        "Skipped in GitHub Actions because it unexplicably (so far) fails there",
    )
    def test_git_url_of_base_juno_pipeline(self) -> None:
        """Testing if the git URL is retrieved properly (taking this folder
        as example
        """
        try:
            is_repo = subprocess.check_output(
                ["git", "rev-parse", "--git-dir"], cwd=main_script_path
            )
        except:
            self.skipTest(
                "The directory containint this package is not a git repo, therefore test was skipped"
            )

        url = get_repo_url(main_script_path)
        self.assertIn(
            url,
            [
                "https://github.com/RIVM-bioinformatics/juno-library.git",
                "git@github.com:RIVM-bioinformatics/juno-library.git",
            ],
        )

    def test_fail_when_dir_not_repo(self) -> None:
        """Testing that the url is 'not available' when the directory is not
        a git repo
        """
        self.assertEqual(
            get_repo_url(os.path.expanduser("~")),
            "Not available. This might be because this folder is not a repository or it was downloaded manually instead of through the command line.",
        )

    @unittest.skipIf(
        not Path("/data/BioGrid/hernanda/").exists(),
        "Skipped in GitHub Actions because it unexplicably (so far) fails there",
    )
    def test_get_commit_git_from_repo(self) -> None:
        """Testing that the git commit function works"""
        try:
            is_repo = subprocess.check_output(
                ["git", "rev-parse", "--git-dir"], cwd=main_script_path
            )
        except:
            self.skipTest(
                "The directory containint this package is not a git repo, therefore test was skipped"
            )
        commit_available = (
            get_commit_git(main_script_path)
            == "Not available. This might be because this folder is not a repository or it was downloaded manually instead of through the command line."
        )
        self.assertIsInstance(get_commit_git(main_script_path), str)
        self.assertFalse(commit_available)

    def test_get_commit_git_from_non_git_repo(self) -> None:
        """Testing that the git commit function gives right output when no git repo"""
        self.assertIsInstance(get_commit_git(os.path.expanduser("~")), str)
        self.assertEqual(
            get_commit_git(os.path.expanduser("~")),
            "Not available. This might be because this folder is not a repository or it was downloaded manually instead of through the command line.",
        )


class TestPipelineStartup(unittest.TestCase):
    """Testing the pipeline startup (generating dict with samples) from general
    Juno pipelines"""

    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        """Making fake directories and files to test different case scenarios
        for starting pipeline"""
        fake_dirs = [
            "fake_dir_empty",
            "fake_dir_wsamples",
            "fake_dir_wsamples/reference",
            "fake_dir_wsamples_exclusion",
            "exclusion_file",
            "fake_dir_incomplete",
            "fake_dir_juno",
            "fake_dir_juno/clean_fastq",
            "fake_dir_juno/de_novo_assembly_filtered",
            "fake_dir_juno/identify_species",
            "fake_1_in_fastqname",
            "fake_multiple_library_samples",
            "fake_dir_juno_assembly_output",
            "fake_dir_juno_mapping_output",
            "fake_dir_juno_variant_typing_output",
            "fake_dir_juno_cgmlst_output",
            "fake_dir_wsamples_juno_cgmlst",
        ]

        fake_files = [
            "fake_dir_wsamples/sample1_R1.fastq",
            "fake_dir_wsamples/sample1_R2.fastq.gz",
            "fake_dir_wsamples/sample2_R1_filt.fq",
            "fake_dir_wsamples/sample2_R2_filt.fq.gz",
            "fake_dir_wsamples/sample1.fasta",
            "fake_dir_wsamples/sample2.fasta",
            "fake_dir_wsamples/sample1.vcf",
            "fake_dir_wsamples/sample2.vcf",
            "fake_dir_wsamples/reference/reference.fasta",
            "fake_dir_wsamples_exclusion/sample1_R1.fastq",
            "fake_dir_wsamples_exclusion/sample1_R2.fastq.gz",
            "fake_dir_wsamples_exclusion/sample2_R1_filt.fq",
            "fake_dir_wsamples_exclusion/sample2_R2_filt.fq.gz",
            "fake_dir_wsamples_exclusion/sample1.fasta",
            "fake_dir_wsamples_exclusion/sample2.fasta",
            "exclusion_file.exclude",
            "fake_dir_incomplete/sample1_R1.fastq",
            "fake_dir_incomplete/sample1_R2.fastq.gz",
            "fake_dir_incomplete/sample2_R1_filt.fq",
            "fake_dir_incomplete/sample2_R2_filt.fq.gz",
            "fake_dir_incomplete/sample2.fasta",
            "fake_dir_juno/clean_fastq/1234_R1.fastq.gz",
            "fake_dir_juno/clean_fastq/1234_R2.fastq.gz",
            "fake_dir_juno/de_novo_assembly_filtered/1234.fasta",
            "fake_1_in_fastqname/1234_1_R1.fastq.gz",
            "fake_1_in_fastqname/1234_1_R2.fastq.gz",
            "fake_multiple_library_samples/sample5_S1_L001_R1.fastq.gz",
            "fake_multiple_library_samples/sample5_S1_L001_R2.fastq.gz",
            "fake_multiple_library_samples/sample5_S1_L002_R1.fastq.gz",
            "fake_multiple_library_samples/sample5_S1_L002_R2.fastq.gz",
        ]

        for folder in fake_dirs:
            Path(folder).mkdir(exist_ok=True, parents=True)
        for file_ in fake_files:
            make_non_empty_file(file_)
        bracken_dir = Path("fake_dir_juno").joinpath("identify_species")
        bracken_dir.mkdir(parents=True, exist_ok=True)
        bracken_multireport_path = bracken_dir.joinpath("top1_species_multireport.csv")
        bracken_multireport_content = "sample,genus,species\n1234,salmonella,enterica\n"
        make_non_empty_file(
            bracken_multireport_path, content=bracken_multireport_content
        )

        for fake_file in fake_files:
            if fake_file == "exclusion_file.exclude":
                make_non_empty_file(fake_file, content="sample1")

    @classmethod
    def tearDownClass(cls) -> None:
        """Removing fake directories/files"""
        fake_dirs = [
            "fake_dir_empty",
            "fake_dir_wsamples",
            "fake_dir_wsamples_library_names",
            "fake_dir_wsamples_exclusion",
            "exclusion_file",
            "fake_dir_incomplete",
            "fake_dir_juno",
            "fake_dir_juno/clean_fastq",
            "fake_dir_juno/de_novo_assembly_filtered",
            "fake_dir_juno/identify_species",
            "fake_1_in_fastqname",
            "fake_multiple_library_samples",
            "fake_dir_juno_assembly_output",
            "fake_dir_juno_mapping_output",
            "fake_dir_juno_variant_typing_output",
            "fake_dir_juno_cgmlst_output",
            "fake_dir_wsamples_juno_cgmlst",
        ]

        for folder in fake_dirs:
            os.system("rm -rf {}".format(str(folder)))

    def test_nonexisting_dir(self) -> None:
        """Testing the pipeline startup fails if the input directory does not
        exist"""
        with self.assertRaises(AssertionError):
            pipeline = Pipeline(**default_args, argv=["-i", "non_existant_dir"])
            pipeline.setup()

    def test_if_excludefile_exists(self) -> None:
        """Testing if the exclude file exists and if there is none that the pipeline continues."""
        with self.assertRaises(FileNotFoundError):
            pipeline = Pipeline(
                **default_args,
                argv=[
                    "-i",
                    "fake_dir_wsamples",
                    "-ex",
                    "exclusion_file_non_existing.exclude",
                ],
            )
            pipeline.setup()

    def test_emptydir(self) -> None:
        """Testing the pipeline startup fails if the input directory does not
        have expected files"""
        with self.assertRaises(ValueError):
            pipeline = Pipeline(
                **default_args, argv=["-i", "fake_dir_empty"], input_type="fastq"
            )
            pipeline.setup()

    def test_incompletedir(self) -> None:
        """Testing the pipeline startup fails if the input directory is
        missing some of the fasta files for the fastq files"""
        with self.assertRaisesRegex(KeyError, "assembly is missing for sample sample1"):
            pipeline = Pipeline(
                **default_args, argv=["-i", "fake_dir_incomplete"], input_type="both"
            )
            pipeline.setup()

    def test_correctdir_fastq(self) -> None:
        """Testing the pipeline startup accepts fastq and fastq.gz files"""

        expected_output = {
            "sample1": {
                "R1": str(
                    Path("fake_dir_wsamples").joinpath("sample1_R1.fastq").resolve()
                ),
                "R2": str(
                    Path("fake_dir_wsamples").joinpath("sample1_R2.fastq.gz").resolve()
                ),
            },
            "sample2": {
                "R1": str(
                    Path("fake_dir_wsamples").joinpath("sample2_R1_filt.fq").resolve()
                ),
                "R2": str(
                    Path("fake_dir_wsamples")
                    .joinpath("sample2_R2_filt.fq.gz")
                    .resolve()
                ),
            },
        }
        pipeline = Pipeline(
            **default_args, argv=["-i", "fake_dir_wsamples"], input_type="fastq"
        )
        pipeline.setup()
        self.assertDictEqual(pipeline.sample_dict, expected_output)

    def test_excludefile(self) -> None:
        """Testing the pipeline startup accepts and works with exclusion file on fastq and fastq.gz files"""
        expected_output = {
            "sample2": {
                "R1": str(
                    Path("fake_dir_wsamples_exclusion")
                    .joinpath("sample2_R1_filt.fq")
                    .resolve()
                ),
                "R2": str(
                    Path("fake_dir_wsamples_exclusion")
                    .joinpath("sample2_R2_filt.fq.gz")
                    .resolve()
                ),
            }
        }
        pipeline = Pipeline(
            **default_args,
            argv=["-i", "fake_dir_wsamples_exclusion", "-ex", "exclusion_file.exclude"],
            input_type="fastq",
        )
        pipeline.setup()
        self.assertDictEqual(pipeline.sample_dict, expected_output)

    def test_correctdir_fastq_with_library_in_filename(self) -> None:
        """Testing the pipeline startup accepts fastq and fastq.gz files"""

        input_dir = Path("fake_dir_wsamples_library_names").resolve()
        input_dir.mkdir(exist_ok=True, parents=True)

        make_non_empty_file(input_dir.joinpath("sample1_R1.fastq"))
        make_non_empty_file(input_dir.joinpath("sample1_R2.fastq.gz"))
        make_non_empty_file(input_dir.joinpath("sample2_R1_filt.fq"))
        make_non_empty_file(input_dir.joinpath("sample2_R2_filt.fq.gz"))
        make_non_empty_file(input_dir.joinpath("sample3_S182_L555_R1_001.fastq.gz"))
        make_non_empty_file(input_dir.joinpath("sample3_S182_L555_R2_001.fastq.gz"))
        make_non_empty_file(input_dir.joinpath("sample4_S183_L001_R1_001.fastq.gz"))
        make_non_empty_file(input_dir.joinpath("sample4_S183_L001_R2_001.fastq.gz"))

        expected_output = {
            "sample1": {
                "R1": str(input_dir.joinpath("sample1_R1.fastq")),
                "R2": str(input_dir.joinpath("sample1_R2.fastq.gz")),
            },
            "sample2": {
                "R1": str(input_dir.joinpath("sample2_R1_filt.fq")),
                "R2": str(input_dir.joinpath("sample2_R2_filt.fq.gz")),
            },
            "sample3": {
                "R1": str(input_dir.joinpath("sample3_S182_L555_R1_001.fastq.gz")),
                "R2": str(input_dir.joinpath("sample3_S182_L555_R2_001.fastq.gz")),
            },
            "sample4": {
                "R1": str(input_dir.joinpath("sample4_S183_L001_R1_001.fastq.gz")),
                "R2": str(input_dir.joinpath("sample4_S183_L001_R2_001.fastq.gz")),
            },
        }
        pipeline = Pipeline(
            **default_args, argv=["-i", str(input_dir)], input_type="fastq"
        )
        pipeline.setup()
        self.assertDictEqual(pipeline.sample_dict, expected_output)

    def test_correctdir_fasta(self) -> None:
        """Testing the pipeline startup accepts fasta"""

        expected_output = {
            "sample1": {
                "assembly": str(
                    Path("fake_dir_wsamples").joinpath("sample1.fasta").resolve()
                )
            },
            "sample2": {
                "assembly": str(
                    Path("fake_dir_wsamples").joinpath("sample2.fasta").resolve()
                )
            },
        }
        pipeline = Pipeline(
            **default_args, argv=["-i", "fake_dir_wsamples"], input_type="fasta"
        )
        pipeline.setup()
        self.assertDictEqual(pipeline.sample_dict, expected_output)

    def test_correctdir_both(self) -> None:
        """Testing the pipeline startup accepts both types"""

        expected_output = {
            "sample1": {
                "R1": str(
                    Path("fake_dir_wsamples").joinpath("sample1_R1.fastq").resolve()
                ),
                "R2": str(
                    Path("fake_dir_wsamples").joinpath("sample1_R2.fastq.gz").resolve()
                ),
                "assembly": str(
                    Path("fake_dir_wsamples").joinpath("sample1.fasta").resolve()
                ),
            },
            "sample2": {
                "R1": str(
                    Path("fake_dir_wsamples").joinpath("sample2_R1_filt.fq").resolve()
                ),
                "R2": str(
                    Path("fake_dir_wsamples")
                    .joinpath("sample2_R2_filt.fq.gz")
                    .resolve()
                ),
                "assembly": str(
                    Path("fake_dir_wsamples").joinpath("sample2.fasta").resolve()
                ),
            },
        }
        pipeline = Pipeline(
            **default_args, argv=["-i", "fake_dir_wsamples"], input_type="both"
        )
        pipeline.setup()
        pipeline.get_metadata_from_csv_file()
        self.assertDictEqual(pipeline.sample_dict, expected_output)
        self.assertIsNone(pipeline.juno_metadata)

    def test_correctdir_fastq_and_vcf(self) -> None:
        """Testing the pipeline startup accepts both fastq and vcf"""

        expected_output = {
            "sample1": {
                "R1": str(
                    Path("fake_dir_wsamples").joinpath("sample1_R1.fastq").resolve()
                ),
                "R2": str(
                    Path("fake_dir_wsamples").joinpath("sample1_R2.fastq.gz").resolve()
                ),
                "vcf": str(Path("fake_dir_wsamples").joinpath("sample1.vcf").resolve()),
                "reference": str(Path("fake_dir_wsamples").joinpath("reference", "reference.fasta").resolve()),
            },
            "sample2": {
                "R1": str(
                    Path("fake_dir_wsamples").joinpath("sample2_R1_filt.fq").resolve()
                ),
                "R2": str(
                    Path("fake_dir_wsamples")
                    .joinpath("sample2_R2_filt.fq.gz")
                    .resolve()
                ),
                "vcf": str(Path("fake_dir_wsamples").joinpath("sample2.vcf").resolve()),
                "reference": str(Path("fake_dir_wsamples").joinpath("reference", "reference.fasta").resolve()),
            },
        }
        pipeline = Pipeline(
            **default_args, argv=["-i", "fake_dir_wsamples"], input_type="fastq_and_vcf"
        )
        pipeline.setup()
        pipeline.get_metadata_from_csv_file()
        self.assertDictEqual(pipeline.sample_dict, expected_output)
        self.assertIsNone(pipeline.juno_metadata)

    def test_correctdir_cgmlst(self) -> None:
        """Testing the pipeline startup accepts juno-cgmlst"""

        input_dir = Path("fake_dir_wsamples_juno_cgmlst").resolve()
        input_dir.mkdir(exist_ok=True, parents=True)
        input_dir.joinpath("cgmlst", "escherichia", "per_sample").mkdir(exist_ok=True, parents=True)
        input_dir.joinpath("cgmlst", "stec", "per_sample").mkdir(exist_ok=True, parents=True)
        input_dir.joinpath("cgmlst", "shigella", "per_sample").mkdir(exist_ok=True, parents=True)
        input_dir.joinpath("audit_trail").mkdir(exist_ok=True, parents=True)

        make_non_empty_file(input_dir.joinpath("cgmlst", "escherichia", "per_sample", "sample1.tsv"))
        make_non_empty_file(input_dir.joinpath("cgmlst", "stec", "per_sample", "sample1.tsv"))
        make_non_empty_file(input_dir.joinpath("cgmlst", "shigella", "per_sample", "sample1.tsv"))

        expected_output = {
            "sample1": {
                "cgmlst_escherichia": str(
                    Path("fake_dir_wsamples_juno_cgmlst").joinpath("cgmlst","escherichia","per_sample","sample1.tsv").resolve()
                ),
                "cgmlst_stec": str(
                    Path("fake_dir_wsamples_juno_cgmlst").joinpath("cgmlst","stec","per_sample","sample1.tsv").resolve()
                ),
                "cgmlst_shigella": str(
                    Path("fake_dir_wsamples_juno_cgmlst").joinpath("cgmlst","shigella","per_sample","sample1.tsv").resolve()
                ),
            },
        }
        pipeline = Pipeline(
            **default_args, argv=["-i", "fake_dir_wsamples_juno_cgmlst"],
        )
        with self.assertRaises(NotImplementedError):
            pipeline.setup()
            self.assertDictEqual(pipeline.sample_dict, expected_output)

    def test_correctdir_with_input_type_as_list(self) -> None:
        """Testing the pipeline startup accepts both types"""

        expected_output = {
            "sample1": {
                "R1": str(
                    Path("fake_dir_wsamples").joinpath("sample1_R1.fastq").resolve()
                ),
                "R2": str(
                    Path("fake_dir_wsamples").joinpath("sample1_R2.fastq.gz").resolve()
                ),
                "assembly": str(
                    Path("fake_dir_wsamples").joinpath("sample1.fasta").resolve()
                ),
            },
            "sample2": {
                "R1": str(
                    Path("fake_dir_wsamples").joinpath("sample2_R1_filt.fq").resolve()
                ),
                "R2": str(
                    Path("fake_dir_wsamples")
                    .joinpath("sample2_R2_filt.fq.gz")
                    .resolve()
                ),
                "assembly": str(
                    Path("fake_dir_wsamples").joinpath("sample2.fasta").resolve()
                ),
            },
        }
        pipeline = Pipeline(
            **default_args, argv=["-i", "fake_dir_wsamples"], input_type=["fastq", "fasta"]
        )
        pipeline.setup()
        pipeline.get_metadata_from_csv_file()
        print(pipeline.sample_dict)
        self.assertDictEqual(pipeline.sample_dict, expected_output)
        self.assertIsNone(pipeline.juno_metadata)

    def test_recognize_juno_assembly_output(self) -> None:
        """
        Testing that the pipeline recognizes the output of the Juno assembly pipeline
        """

        input_dir = Path("fake_dir_juno_assembly_output").resolve()
        input_dir.mkdir(exist_ok=True, parents=True)
        input_dir.joinpath("clean_fastq").mkdir(exist_ok=True, parents=True)
        input_dir.joinpath("de_novo_assembly_filtered").mkdir(exist_ok=True, parents=True)

        make_non_empty_file(input_dir.joinpath("clean_fastq", "sample_A_R1.fastq.gz"))
        make_non_empty_file(input_dir.joinpath("clean_fastq", "sample_A_R2.fastq.gz"))
        make_non_empty_file(input_dir.joinpath("de_novo_assembly_filtered", "sample_A.fasta"))

        pipeline = Pipeline(
            **default_args, argv=["-i", str(input_dir)], input_type="both"
        )
        pipeline.setup()
        self.assertTrue(pipeline.input_dir_is_juno_assembly_output)

        pipeline_input_type_list = Pipeline(
            **default_args, argv=["-i", str(input_dir)], input_type=["fastq", "fasta"]
        )
        pipeline_input_type_list.setup()
        self.assertTrue(pipeline_input_type_list.input_dir_is_juno_assembly_output)


    def test_recognize_juno_mapping_output(self) -> None:
        """
        Testing that the pipeline recognizes the output of the Juno mapping pipeline
        """

        input_dir = Path("fake_dir_juno_mapping_output").resolve()
        input_dir.mkdir(exist_ok=True, parents=True)
        input_dir.joinpath("mapped_reads", "duprem").mkdir(exist_ok=True, parents=True)
        input_dir.joinpath("variants").mkdir(exist_ok=True, parents=True)
        input_dir.joinpath("reference").mkdir(exist_ok=True, parents=True)

        make_non_empty_file(input_dir.joinpath("mapped_reads", "duprem", "sample_A.bam"))
        make_non_empty_file(input_dir.joinpath("variants", "sample_A.vcf"))
        make_non_empty_file(input_dir.joinpath("reference", "reference.fasta"))

        pipeline = Pipeline(
            **default_args, argv=["-i", str(input_dir)], input_type=["bam", "vcf"]
        )
        pipeline.setup()
        self.assertTrue(pipeline.input_dir_is_juno_mapping_output)
    
    def test_recognize_juno_variant_typing_output(self) -> None:
        """
        Testing that the pipeline recognizes the output of the Juno variant typing pipeline
        """

        input_dir = Path("fake_dir_juno_variant_typing_output").resolve()
        input_dir.mkdir(exist_ok=True, parents=True)
        input_dir.joinpath("mtb_typing", "consensus").mkdir(exist_ok=True, parents=True)
        input_dir.joinpath("audit_trail").mkdir(exist_ok=True, parents=True)
        
        make_non_empty_file(input_dir.joinpath("mtb_typing", "consensus", "sample_A.fasta"))
        
        pipeline = Pipeline(
            **default_args, argv=["-i", str(input_dir)], input_type=["fasta"]
        )
        pipeline.setup()
        self.assertTrue(pipeline.input_dir_is_juno_variant_typing_output)

    def test_recognize_juno_cgmlst_output(self) -> None:
        """
        Testing that the pipeline recognizes the output of the Juno cgmlst pipeline
        """

        input_dir = Path("fake_dir_juno_cgmlst_output").resolve()
        input_dir.mkdir(exist_ok=True, parents=True)
        input_dir.joinpath("cgmlst", "escherichia", "per_sample").mkdir(exist_ok=True, parents=True)
        input_dir.joinpath("cgmlst", "shigella", "per_sample").mkdir(exist_ok=True, parents=True)
        input_dir.joinpath("cgmlst", "stec", "per_sample").mkdir(exist_ok=True, parents=True)
        input_dir.joinpath("audit_trail").mkdir(exist_ok=True, parents=True)
        
        make_non_empty_file(input_dir.joinpath("cgmlst", "escherichia", "per_sample", "sample_A.tsv"))
        make_non_empty_file(input_dir.joinpath("cgmlst", "stec", "per_sample", "sample_A.tsv"))
        make_non_empty_file(input_dir.joinpath("cgmlst", "shigella", "per_sample", "sample_A.tsv"))
        
        pipeline = Pipeline(
            **default_args, argv=["-i", str(input_dir)],
        )
        with self.assertRaises(NotImplementedError):
            pipeline.setup()
            self.assertTrue(pipeline.input_dir_is_juno_cgmlst_output)

    def test_files_smaller_than_minlen(self) -> None:
        """Testing the pipeline startup fails if you set a min_num_lines
        different than 0"""

        with self.assertRaisesRegex(ValueError, "does not contain any files"):
            pipeline = Pipeline(
                **default_args,
                argv=["-i", "fake_dir_incomplete"],
                input_type="both",
                min_num_lines=1000,
            )
            pipeline.setup()

    def test_junodir_wnumericsamplenames(self) -> None:
        """Testing the pipeline startup converts numeric file names to
        string"""

        expected_output = {
            "1234": {
                "R1": str(
                    Path("fake_dir_juno")
                    .joinpath("clean_fastq", "1234_R1.fastq.gz")
                    .resolve()
                ),
                "R2": str(
                    Path("fake_dir_juno")
                    .joinpath("clean_fastq", "1234_R2.fastq.gz")
                    .resolve()
                ),
                "assembly": str(
                    Path("fake_dir_juno")
                    .joinpath("de_novo_assembly_filtered", "1234.fasta")
                    .resolve()
                ),
            }
        }
        expected_metadata = {"1234": {"genus": "salmonella", "species": "enterica"}}
        pipeline = Pipeline(
            **default_args,
            argv=["-i", "fake_dir_juno"],
            input_type="both",
        )
        pipeline.setup()
        pipeline.get_metadata_from_csv_file()
        self.assertDictEqual(pipeline.sample_dict, expected_output)
        assert pipeline.juno_metadata is not None
        self.assertDictEqual(
            pipeline.juno_metadata, expected_metadata, pipeline.juno_metadata
        )

    def test_fail_with_1_in_fastqname(self) -> None:
        """Testing the pipeline startup fails with wrong fastq naming (name
        contains _1_ in the sample name)"""
        with self.assertRaises(KeyError):
            pipeline = Pipeline(
                **default_args,
                argv=["-i", "fake_1_in_fastqname"],
                input_type="fastq",
            )
            pipeline.setup()

    def test_fail_with_multiple_libraries_per_sample(self) -> None:
        """Testing the pipeline startup fails with wrong fastq naming (multiple libraries per sample)"""
        with self.assertRaises(KeyError):
            pipeline = Pipeline(
                **default_args,
                argv=["-i", "fake_multiple_library_samples"],
                input_type="fastq",
            )
            pipeline.setup()

    def test_fails_if_metadata_has_wrong_colnames(self) -> None:
        """
        Testing the pipeline startup fails with wrong column names in metadata
        """
        pipeline = Pipeline(**default_args, argv=["-i", "fake_dir_juno"])
        pipeline.setup()
        with self.assertRaisesRegex(
            AssertionError, "does not contain one or more of the expected column names"
        ):
            pipeline.get_metadata_from_csv_file(expected_colnames=["Sample", "Genus"])


class TestRunSnakemake(unittest.TestCase):
    """Testing the RunSnakemake class. At least testing that it is constructed
    properly (not testing the run itself)"""

    @classmethod
    def setUpClass(cls) -> None:
        with open("user_parameters.yaml", "a") as file_:
            file_.write("fake_parameter: null")
        with open("fixed_parameters.yaml", "a") as file_:
            file_.write("fake_parameter: null")
        with open("sample_sheet.yaml", "a") as file_:
            file_.write("fake_sample: null")
        os.mkdir("fake_input")
        Path("fake_input/sample_a.fasta").touch()
        Path("fake_input/sample_b.fasta").touch()
        Path("fake_input/sample_c.fasta").touch()
        make_non_empty_file(Path("fake_input/sample11233_R1.fastq"))
        make_non_empty_file(Path("fake_input/sample11233_R2.fastq"))

    @classmethod
    def tearDownClass(cls) -> None:
        os.system("rm sample_sheet.yaml user_parameters.yaml fixed_parameters.yaml")
        os.system("rm -rf fake_output_dir")
        os.system("rm -rf fake_hpcoutput_dir")
        os.system("rm -rf fake_input")
        os.system("rm -rf exclusion_file.exclude")

    def test_fake_dryrun_setup(self) -> None:
        argv = [
            # "library_tests.py",
            "-i",
            "fake_input",
            "-o",
            "fake_output_dir",
            "-n",  # dryrun
            "--local",
        ]
        fake_run = Pipeline(
            argv=argv,
            # input_dir=Path("fake_input"),
            input_type="fastq",
            pipeline_name="fake_pipeline",
            pipeline_version="0.1",
            sample_sheet=Path("sample_sheet.yaml"),
            user_parameters_file=Path("user_parameters.yaml"),
        )
        fake_run.snakefile = str(Path("tests/Snakefile").resolve())
        fake_run.run()
        audit_trail_path = Path("fake_output_dir", "audit_trail")
        self.assertIsInstance(fake_run.date_and_time, str)
        self.assertEqual(fake_run.workdir, Path(main_script_path))
        self.assertFalse(Path("fake_output_dir").is_dir())
        self.assertFalse(audit_trail_path.is_dir())
        self.assertFalse(audit_trail_path.joinpath("log_conda.txt").is_file())
        self.assertFalse(audit_trail_path.joinpath("log_git.yaml").is_file())
        self.assertFalse(audit_trail_path.joinpath("log_pipeline.yaml").is_file())
        self.assertFalse(audit_trail_path.joinpath("sample_sheet.yaml").is_file())
        self.assertFalse(audit_trail_path.joinpath("user_parameters.yaml").is_file())
        self.assertFalse(audit_trail_path.joinpath("exclusion_file.exclude").is_file())

    def test_fake_run_setup(self) -> None:
        argv = [
            "-i",
            "fake_input",
            "-o",
            "fake_output_dir",
        ]
        pipeline = Pipeline(
            argv=argv,
            input_type="fastq",
            pipeline_name="fake_pipeline",
            pipeline_version="0.1",
            sample_sheet=Path("sample_sheet.yaml"),
            user_parameters_file=Path("user_parameters.yaml"),
        )
        pipeline.snakefile = str(Path("tests/Snakefile").resolve())
        pipeline.setup()

        pipeline.path_to_audit = Path("fake_output_dir", "audit_trail")
        pipeline._generate_audit_trail()

        self.assertIsInstance(pipeline.date_and_time, str)
        self.assertEqual(pipeline.workdir, Path(main_script_path))
        self.assertTrue(Path("fake_output_dir").is_dir())
        self.assertTrue(pipeline.path_to_audit.is_dir())
        self.assertTrue(pipeline.path_to_audit.joinpath("log_conda.txt").is_file())
        self.assertTrue(pipeline.path_to_audit.joinpath("log_git.yaml").is_file())
        self.assertTrue(pipeline.path_to_audit.joinpath("log_pipeline.yaml").is_file())
        self.assertTrue(pipeline.path_to_audit.joinpath("sample_sheet.yaml").is_file())
        self.assertTrue(
            pipeline.path_to_audit.joinpath("user_parameters.yaml").is_file()
        )
        # self.assertTrue(audit_trail_path.joinpath('exclusion_file.exclude').is_file())

        pipeline_name_in_audit_trail = False
        pipeline_version_in_audit_trail = False
        with open(
            pipeline.path_to_audit.joinpath("log_pipeline.yaml"), "r"
        ) as git_pipeline_trail_file:
            for line in git_pipeline_trail_file:
                if "fake_pipeline" in line:
                    pipeline_name_in_audit_trail = True
                if "0.1" in line:
                    pipeline_version_in_audit_trail = True
        self.assertTrue(pipeline_name_in_audit_trail)
        self.assertTrue(pipeline_version_in_audit_trail)

        try:
            is_repo = Path("/data/BioGrid/hernanda/").exists()
        except:
            is_repo = False

        if is_repo:
            repo_url_in_audit_trail = False
            with open(
                pipeline.path_to_audit.joinpath("log_git.yaml"), "r"
            ) as git_audit_trail_file:
                for line in git_audit_trail_file:
                    if (
                        "https://github.com/RIVM-bioinformatics/juno-library.git"
                        in line
                        or "git@github.com:RIVM-bioinformatics/juno-library.git" in line
                    ):
                        repo_url_in_audit_trail = True
            self.assertTrue(repo_url_in_audit_trail)

    def test_pipeline(self) -> None:
        output_dir = Path("fake_output_dir")
        os.system(f'echo "output_dir: {str(output_dir)}" > user_parameters.yaml')

        argv = [
            "-i",
            "fake_input",
            "-o",
            "fake_output_dir",
            "--local",
        ]
        pipeline = Pipeline(
            argv=argv,
            input_type="fastq",
            **default_args,
        )
        pipeline.snakefile = str(Path("tests/Snakefile").resolve())
        pipeline.run()

        audit_trail_path = output_dir.joinpath("audit_trail")
        pipeline.run()
        self.assertTrue(output_dir.joinpath("fake_result.txt").exists())
        self.assertTrue(audit_trail_path.joinpath("snakemake_report.html").exists())

    @unittest.skipIf(
        not Path("/data/BioGrid/hernanda/").exists(),
        "Skipped if not in RIVM HPC cluster",
    )
    def test_pipeline_in_hpcRIVM(self) -> None:
        output_dir = Path("fake_hpcoutput_dir")
        os.system(f'echo "output_dir: {str(output_dir)}" > user_parameters.yaml')
        pipeline = Pipeline(
            argv=[
                "-i",
                "fake_input",
                "-o",
                str(output_dir),
            ],
            input_type="fastq",
            **default_args,
        )
        pipeline.snakefile = str(Path("tests/Snakefile").resolve())
        audit_trail_path = output_dir.joinpath("audit_trail")
        pipeline.run()
        self.assertTrue(output_dir.joinpath("fake_result.txt").exists())
        self.assertTrue(audit_trail_path.joinpath("snakemake_report.html").exists())


class TestKwargsClass(unittest.TestCase):
    """Testing Argparse action to store kwargs (to be passed to Snakemake)"""

    def test_kwargs_are_parsed(self) -> None:
        parser = argparse.ArgumentParser(description="Testing parser")
        parser.add_argument(
            "--snakemake-args",
            nargs="*",
            default={},
            action=SnakemakeKwargsAction,
            help="Extra arguments to be passed to snakemake API (https://snakemake.readthedocs.io/en/stable/api_reference/snakemake.html).",
        )
        self.assertRaisesRegex(
            argparse.ArgumentTypeError,
            "Make sure that you used the API format",
            lambda: parser.parse_args(
                ["--snakemake-args", "key1->value1", "resources"]
            ),
        )

        self.assertRaisesRegex(
            argparse.ArgumentTypeError,
            "not specified in the snakemake python API",
            lambda: parser.parse_args(["--snakemake-args", "key1=value1"]),
        )

        args = parser.parse_args(
            ["--snakemake-args", "cores=1", "resources={'gpu':1}", "summary=True"]
        )
        expected_output = {"cores": 1, "resources": dict(gpu=1), "summary": True}
        self.assertEqual(args.snakemake_args, expected_output, args.snakemake_args)


if __name__ == "__main__":
    unittest.main()
