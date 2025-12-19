import gc
import os

import ifcopenshell
import multiprocessing as mp
# from core.main_batchid_mesh_types_separation import ifcToGltf
# from core.main import ifcToGltf
from core.main_separation_NormalLine import ifcToGltf
# from core.main_separation import ifcToGltf



if __name__ == '__main__':
    # 加载所需转换的ifc文件
    file_path = './resource/IfcWall.ifc'

    file_name = os.path.basename(file_path).rstrip(os.path.basename(file_path)[-4:])

    # 调用ifcToGltf方法，转换为gltf数据 （ifc_file为必要参数，file_name为非必要参数）
    # gltf = ifcToGltf(ifc_file, file_name)
    p = mp.Process(target=ifcToGltf, args=(file_path, file_name))
    # run `worker` in a subprocess
    p.start()
    # make the main process wait for `worker` to end
    p.join()
    # all memory used by the subprocess will be freed to the OS

