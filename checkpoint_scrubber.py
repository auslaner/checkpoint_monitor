"""
Script for monitoring the output folder for deep learning checkpoint
files. Each file takes up quite a bit of space, so when disk space
is limited, it makes sense to delete those that are now longer needed
while training continues to generate new ones.

This script aims to keep the most recent checkpoint, and milestone
checkpoints defined by the MILESTONE_CHKPTS variable.
"""
import argparse
import os

MILESTONE_CHKPTS = [50, 60, 70, 80]


def main(model_path):
    for dirpath, dirnames, filenames in os.walk(model_path):
        # Create a dictionary of filenames with their checkpoint numbers
        checkpoints = {filename: int(''.join(filter(str.isdigit, filename.split("-")[-1])))
                       for filename in filenames if ''.join(filter(str.isdigit, filename.split("-")[-1])).isdigit()}

        chkpt_nums = checkpoints.values()
        try:
            end_chkpt_num = max(chkpt_nums)
        except ValueError:
            # No checkpoints
            continue

        chkpts_to_keep = MILESTONE_CHKPTS.copy()
        chkpts_to_keep.append(end_chkpt_num)

        for fname, chkpt_num in checkpoints.items():
            if chkpt_num not in chkpts_to_keep:
                print("Checkpoints to keep:", chkpts_to_keep)
                print("Deleting {}...".format(fname))
                os.remove(os.path.join(dirpath, fname))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--checkpoints", required=True,
                    help="path to output checkpoint directory")
    args = vars(ap.parse_args())

    main(args["checkpoints"])
