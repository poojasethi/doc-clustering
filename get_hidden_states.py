"""
Gets hidden states for a model.
"""

import argparse

from lib.LayoutLM import LayoutLM
from lib.LayoutLMv2 import LayoutLMv2
from lib.path_utils import existing_directory


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "model",
        choices=[
            "vanilla_lmv1",
            "finetuned_lmv1_related",
            "finetuned_lmv1_unrelated",
            "vanilla_lmv2",
            "finetuned_lmv2_related"
        ],
        type=str,
        help="The type of model to obtain embeddings from",
    )
    parser.add_argument(
        "-r",
        "--rivlets-dir",
        type=existing_directory,
        help="Path to directory containing rivlets. Each dataset is assumed to be preprocessed using Impira.",
        required=True,
    )
    parser.add_argument(
        "-e",
        "--embedding-dir",
        type=existing_directory,
        help="Path to directory where hidden states will be pickled and stored.",
        default="embeddings/",
    )

    parser.add_argument(
        "-m",
        "--models-dir",
        type=existing_directory,
        help="Path to directory containing trained models.",
        default="models/",
    )

    parser.add_argument("-b", "--batch-size", type=int, help="Number of examples to get hidden states for at one time")
    parser.add_argument("-f", "--file-type", type = str, help="Image file type e.g. png, tif, jpg")
    return parser


def main(args: argparse.Namespace):
    # PUT DIRECTORY OF RIVLETS HERE
    # rivlets_dir = "/Users/bryanchia/Desktop/stanford/classes/cs/cs224n/project/data/rivlets"
    rivlets_dir = args.rivlets_dir
    embedding_dir = args.embedding_dir

    # OUTPUT VANILLA LM HIDDEN STATES
    if args.model == "vanilla_lmv1":
        i1 = LayoutLM()
        int_data = i1.process_json(rivlets_dir, "processed_word", "location", position_processing=True)

        # outpath = "/Users/bryanchia/Desktop/stanford/classes/cs/cs224n/project/data/encodings/layoutlm_noft_encodings.pkl"
        outpath = args.embedding_dir / "layoutlm_noft_encodings.pkl"

        encodings = i1.get_encodings()
        hidden_state = i1.get_hidden_state(outpath=outpath, batch_size=args.batch_size)

        print(hidden_state)

        print(hidden_state.to_pandas())

    # OUTPUT FINE-TUNED HIDDEN STATES (RELATED TASK)
    elif args.model == "finetuned_lmv1_related":
        i2 = LayoutLM()
        i2.process_json(rivlets_dir, "processed_word", "location", position_processing=True)

        # outpath = "/Users/bryanchia/Desktop/stanford/classes/cs/cs224n/project/data/encodings/layoutlm_ft_encodings.pkl"
        # model_path = "/Users/bryanchia/Desktop/stanford/classes/cs/cs224n/project/models/fine_tuned_related/epoch7"
        outpath = args.embedding_dir / "layoutlm_ft_encodings.pkl"
        model_path = args.models_dir / "fine_tune_related"

        encodings = i2.get_encodings()
        hidden_state = i2.get_hidden_state(outpath=outpath, model_path=model_path)
        print(hidden_state.to_pandas())

    # OUTPUT FINE-TUNED HIDDEN STATES (UNRELATED TASK)
    elif args.model == "finetuned_lmv1_unrelated":
        i3 = LayoutLM()
        i3.process_json(rivlets_dir, "processed_word", "location", position_processing=True)

        # outpath = "/Users/bryanchia/Desktop/stanford/classes/cs/cs224n/project/data/encodings/layoutlm_ft_ur_encodings.pkl"
        # model_path = "/Users/bryanchia/Desktop/stanford/classes/cs/cs224n/project/models/fine_tuned_unrelated/epoch15"
        outpath = args.embedding_dir / "layoutlm_ft_ur_encodings.pkl"
        model_path = args.models_dir / "fine_tuned_unrelated2"

        encodings = i3.get_encodings()
        hidden_state = i3.get_hidden_state(outpath=outpath, model_path=model_path)
        print(hidden_state.to_pandas())

    # OUTPUT VANILLA LM V2 HIDDEN STATES
    elif args.model == "vanilla_lmv2":
        i4 = LayoutLMv2()
        # rivlets_dir  = "/Users/bryanchia/Desktop/stanford/classes/cs/cs224n/project/data/files"
        outpath = args.embedding_dir / "layoutlmv2_noft_encodings.pkl"
        hidden_state = i4.get_outputs(rivlets_dir, outpath = outpath, file_type = args.file_type)
        print(hidden_state.to_pandas())

    # OUTPUT FINE-TUNED HIDDEN STATES (RELATED TASK)
    elif args.model == "finetuned_lmv2_related":
        i5 = LayoutLMv2()

        outpath = args.embedding_dir / "layoutlmv2_ft_encodings.pkl"
        model_path = args.models_dir / "fine_tune_related_v2"
        hidden_state = i5.get_outputs(rivlets_dir, outpath = outpath, model = model_path, file_type = args.file_type)
        print(hidden_state.to_pandas())


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args)
