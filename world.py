from settings import *
from chunk import Chunk

class World:
    
    def __init__(self, chunkShaderProgram):
        
        self.chunkShaderProgram = chunkShaderProgram
        self.chunks = np.empty(WORLD_VOLUME, dtype=np.object_)
        self.chunks_data = np.ones((WORLD_VOLUME, CHUNK_VOLUME))
        self.generate_chunks()
        
        print(f"World size: {self.chunks_data.nbytes / 1024 / 1024} MB")
    
    def render(self, view, projection):
        
        viewLoc = glGetUniformLocation(self.chunkShaderProgram, "view")
        projLoc = glGetUniformLocation(self.chunkShaderProgram, "projection")
        
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(projLoc, 1, GL_FALSE, glm.value_ptr(projection))
        
        for chunk in self.chunks:
            if chunk is not None:
                chunk.render()
                
    def generate_chunks(self):
        for wx in range(WORLD_WIDTH):
            for wz in range(WORLD_HEIGHT):
                for wy in range(WORLD_DEPTH):
                    chunk_world_index = wx + wz * WORLD_WIDTH + wy * WORLD_WIDTH * WORLD_HEIGHT
                    chunk = Chunk(shaderProgram=self.chunkShaderProgram,pos=(wx * CHUNK_SIZE, wy * CHUNK_SIZE, wz * CHUNK_SIZE))
                    chunk.mesh_data = self.build_chunk_mesh(wx, wy, wz)
                    chunk.model_matrix = chunk.create_model_matrix()
                    chunk.ivbo = chunk.setup_ivbo()
                    self.chunks[chunk_world_index] = chunk
        
    def voxel_index(self, x, y, z):
        return x + z * CHUNK_SIZE + y * CHUNK_AREA
        
    def is_void(self, x, y, z, wx, wy, wz):
        
        if 0 <= x < CHUNK_SIZE and 0 <= y < CHUNK_SIZE and 0 <= z < CHUNK_SIZE:
            if self.chunks_data[wx + wz * WORLD_WIDTH + wy * WORLD_WIDTH * WORLD_HEIGHT][self.voxel_index(x, y, z)]:
                return False
            
        return True
        
        xi, yi, zi = x, y, z
        wxi, wyi, wzi = wx, wy, wz
        
        if (x < 0):
            xi = CHUNK_SIZE - 1
            wxi -= 1
            if wxi < 0:
                return True
        elif (x >= CHUNK_SIZE):
            xi = 0
            wxi += 1
            if wxi >= WORLD_WIDTH:
                return True
            
        if (y < 0):
            yi = CHUNK_SIZE - 1
            wyi -= 1
            if wyi < 0:
                return True
        elif (y >= CHUNK_SIZE):
            yi = 0
            wyi += 1
            if wyi >= WORLD_HEIGHT:
                return True
        
        if (z < 0):
            zi = CHUNK_SIZE - 1
            wzi -= 1
            if wzi < 0:
                return True
        elif (z >= CHUNK_SIZE):
            zi = 0
            wzi += 1
            if wzi >= WORLD_DEPTH:
                return True
            
        print(f"\nx:{x} y:{y} z:{z} xi:{xi} yi:{yi} zi:{zi}")
        print(f"wx:{wx} wy:{wy} wz:{wz} wxi:{wxi} wyi:{wyi} wzi:{wzi}")
        
        chunk_world_index = wx + wz * WORLD_WIDTH + wy * WORLD_WIDTH * WORLD_HEIGHT
        voxel_chunk_index = self.voxel_index(xi, yi, zi)
        
        if self.chunks_data[chunk_world_index][voxel_chunk_index] != 0:
            print("Not Void")
            return False
        
        return True
        
    def build_chunk_mesh(self, wx, wy, wz):
        chunk_index = wx + wz * WORLD_WIDTH + wy * WORLD_WIDTH * WORLD_HEIGHT
        chunk = self.chunks[chunk_index]
        
        chunk_instance_data = np.zeros((CHUNK_VOLUME * 3, 4), dtype=np.uint8)
        index = 0
        
        for x in range(CHUNK_SIZE):
            for y in range(CHUNK_SIZE):
                for z in range(CHUNK_SIZE):
                    voxel_index = self.voxel_index(x, y, z)
                    voxel_id = self.chunks_data[chunk_index][voxel_index]
                    
                    if not voxel_id:
                        continue
                    
                    if self.is_void( x, y + 1, z, wx, wy, wz):
                        face_data = np.array([
                            0, x, y, z,
                        ], dtype=np.uint8)
                        chunk_instance_data[index] = face_data
                        index += 1
                        
                    # if self.is_void( x, y - 1, z, wx, wy, wz):
                    #     face_data = np.array([
                    #         1, x, y, z,
                    #     ], dtype=np.uint8)
                    #     chunk_instance_data[index] = face_data
                    #     index += 1
                        
                    if self.is_void( x - 1, y, z, wx, wy, wz):
                        face_data = np.array([
                            2, x, y, z,
                        ], dtype=np.uint8)
                        chunk_instance_data[index] = face_data
                        index += 1
                        
                    if self.is_void( x + 1, y, z, wx, wy, wz):
                        face_data = np.array([
                            3, x, y, z,
                        ], dtype=np.uint8)
                        chunk_instance_data[index] = face_data
                        index += 1
                        
                    if self.is_void( x, y, z - 1, wx, wy, wz):
                        face_data = np.array([
                            4, x, y, z,
                        ], dtype=np.uint8)
                        chunk_instance_data[index] = face_data
                        index += 1
                    
                    if self.is_void( x, y, z + 1, wx, wy, wz):
                        face_data = np.array([
                            5, x, y, z,
                        ], dtype=np.uint8)
                        chunk_instance_data[index] = face_data
                        index += 1
                        
        return chunk_instance_data[: index]
                