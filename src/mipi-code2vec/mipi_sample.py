import json

from mipi.base_codemeaning_predictor import PatchInfo
from mipi.mipi_app import Mipi


def load_patches_from_file(patches_json_file):
    with open(patches_json_file, "r", encoding="utf8") as file:
        patches_json = json.load(file)
    patches = []
    for jo_patch in patches_json:
        patch = PatchInfo()
        patch.from_json(jo_patch)
        patches.append(patch)
    return patches


if __name__ == '__main__':
 
    dataset_json_file = 'SamplePatches.json'
    patches = load_patches_from_file(dataset_json_file)

    obj_mipi = Mipi()

    for p in patches:
        rs = obj_mipi.evaluate(p)
        print('Results: \n%s' % rs)
        print('Json resuls: \n%s' % rs.to_json())
