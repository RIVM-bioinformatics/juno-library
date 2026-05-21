import pathlib
import argparse
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from juno_library import Pipeline
import yaml
import tempfile


def create_mock_nanopore_output(base_dir):
    fastplong_dir = base_dir / "fastplong"
    flye_dir = base_dir / "flye"
    fastplong_dir.mkdir()
    flye_dir.mkdir()
    # Create barcode folders with fastq files
    for barcode in ["barcode01", "barcode02"]:
        barcode_dir = fastplong_dir / barcode
        barcode_dir.mkdir()
        (barcode_dir / f"{barcode}.fastq.gz").write_text("FAKEFASTQ")
    # Create assemblies in flye/barcode/barcode.fasta
    for barcode in ["barcode01", "barcode02"]:
        barcode_flye_dir = flye_dir / barcode
        barcode_flye_dir.mkdir()
        (barcode_flye_dir / f"{barcode}.fasta").write_text(">contig\nACTG")


def test_pipeline(input_dir, sequencing_tech):
    pipeline = Pipeline(
        pipeline_name="test_pipeline",
        pipeline_version="1.0",
        input_type="fastq",
        argv=[
            "--input",
            str(input_dir),
            "--output",
            "output",
            "--sequencing-tech",
            sequencing_tech,
        ],
    )
    pipeline.setup()
    return pipeline.sample_dict


def test_illumina():
    illumina_input_dir = pathlib.Path("examples/illumina_example")
    illumina_sample_dict = test_pipeline(illumina_input_dir, "illumina")
    print("Illumina Sample Dict:")
    print(illumina_sample_dict)


def test_nanopore():
    nanopore_input_dir = pathlib.Path("examples/nanopore_example")
    nanopore_sample_dict = test_pipeline(nanopore_input_dir, "nanopore")
    print("Nanopore Sample Dict:")
    print(nanopore_sample_dict)


def test_real_nanopore_output_sample_dict():
    real_nanopore_dir = pathlib.Path("examples/nanopore_output_example")
    pipeline = Pipeline(
        pipeline_name="test_nanopore",
        pipeline_version="1.0",
        input_type="fastq",
        argv=[
            "--input",
            str(real_nanopore_dir),
            "--output",
            str(real_nanopore_dir / "output"),
            "--sequencing-tech",
            "nanopore",
        ],
    )
    pipeline.setup()
    print("Sample dict:")
    print(yaml.dump(pipeline.sample_dict, default_flow_style=False))


def test_nanopore_output_sample_dict():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = pathlib.Path(tmpdir)
        create_mock_nanopore_output(tmp_path)
        pipeline = Pipeline(
            pipeline_name="test_nanopore",
            pipeline_version="1.0",
            input_type="fastq",
            argv=[
                "--input",
                str(tmp_path),
                "--output",
                str(tmp_path / "output"),
                "--sequencing-tech",
                "nanopore",
            ],
        )
        pipeline.setup()
        print("Sample dict:")
        print(yaml.dump(pipeline.sample_dict, default_flow_style=False))


def main():
    parser = argparse.ArgumentParser(
        description="Test sample dictionary building for different sequencing technologies."
    )
    parser.add_argument(
        "--tech",
        choices=["illumina", "nanopore", "both", "nanopore_output"],
        required=True,
        help="Specify the sequencing technology to test.",
    )
    args = parser.parse_args()

    if args.tech == "illumina":
        print("Running Illumina Test:")
        test_illumina()
    elif args.tech == "nanopore":
        print("Running Nanopore Test:")
        test_nanopore()
    elif args.tech == "both":
        print("Running Illumina Test:")
        test_illumina()
        print("\nRunning Nanopore Test:")
        test_nanopore()
    elif args.tech == "nanopore_output":
        print("Running Real Nanopore Output Test:")
        # test_nanopore_output_sample_dict()
        test_real_nanopore_output_sample_dict()


if __name__ == "__main__":
    main()
