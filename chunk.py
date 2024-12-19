from settings import *

class Chunk():
    
    def __init__(self):
        
        self.chunk_position = (0, 0, 0)
        self.chunk_data = self.build_chunk()
        self.mesh_data = self.build_mesh()
        
    def voxel_index(self, x, y, z):
        return x + z * CHUNK_SIZE + y * CHUNK_AREA
        
    def build_chunk(self):
        return np.ones(CHUNK_VOLUME, dtype=np.uint8)
        np.random.seed(0)
        return np.random.randint(0, 2, CHUNK_VOLUME, dtype=np.uint8)
    
    def is_void(self, x, y, z):
        
        if 0 <= x < CHUNK_SIZE and 0 <= y < CHUNK_SIZE and 0 <= z < CHUNK_SIZE:
            if self.chunk_data[self.voxel_index(x, y, z)]:
                return False
        return True
        
    def build_mesh(self):
        chunk_instance_data = np.empty((CHUNK_VOLUME * 3, 4), dtype=np.uint8)
        index = 0
        
        for x in range(CHUNK_SIZE):
            for y in range(CHUNK_SIZE):
                for z in range(CHUNK_SIZE):
                    voxel_index = self.voxel_index(x, y, z)
                    voxel_id = self.chunk_data[voxel_index]
                    
                    if not voxel_id:
                        continue
                    
                    # Top Face
                    if self.is_void( x, y + 1, z ):
                        
                        face_data = np.array([
                            0, x, y, z,
                        ], dtype=np.uint8)
                        chunk_instance_data[index] = face_data
                        index += 1
                        
                    # Bottom Face
                    if self.is_void( x, y-1, z ):
                        
                        face_data = np.array([
                            1, x, y, z
                        ], dtype=np.uint8)
                        chunk_instance_data[index] = face_data
                        index += 1
                        
                    # Left Face
                    if self.is_void( x-1, y, z ):
                        
                        face_data = np.array([
                            2, x, y, z
                        ], np.uint8)
                        chunk_instance_data[index] = face_data
                        index += 1
        
                    # Right Face
                    if self.is_void( x+1, y, z ):
                        
                        face_data = np.array([
                            3, x, y, z
                        ], np.uint8)
                        chunk_instance_data[index] = face_data
                        index += 1
                        
                    # Front Face
                    if self.is_void( x, y, z-1 ):
                        
                        face_data = np.array([
                            4, x, y, z
                        ], np.uint8)
                        chunk_instance_data[index] = face_data
                        index += 1
                        
                    # Back Face
                    if self.is_void( x, y, z+1):
                        
                        face_data = np.array([
                            5, x, y, z
                        ], np.uint8)
                        chunk_instance_data[index] = face_data
                        index += 1
                        
        print(index)
        return chunk_instance_data[: index + 1]