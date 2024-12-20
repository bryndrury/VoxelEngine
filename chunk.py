from settings import *

class Chunk():
    
    def __init__(self, shaderProgram, pos=(0,0,0)):
        self.shaderProgram = shaderProgram
        self.chunk_position = pos
        self.chunk_data = self.build_chunk()
        self.mesh_data = self.build_mesh()
        
        self.model_matrix = self.create_model_matrix()
        self.ivbo = self.setup_ivbo() # Instance VBO
        
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
                        
        return chunk_instance_data[: index + 1]
    
    
    def create_model_matrix(self):
        model_matrix = glm.mat4(1)
        model_matrix = glm.translate(model_matrix, glm.vec3(self.chunk_position))
        return model_matrix
    
    
    def use_model_matrix(self):
        glUseProgram(self.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(self.shaderProgram, "chunk_model"), 1, GL_FALSE, glm.value_ptr(self.model_matrix))
    
    
    def setup_ivbo(self):
        
        instance_vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, instance_vbo)
        glBufferData(GL_ARRAY_BUFFER, self.mesh_data.nbytes, self.mesh_data, GL_STATIC_DRAW)
        glVertexAttribIPointer(1, 4, GL_UNSIGNED_BYTE, 4, ctypes.c_void_p(0))
        glVertexAttribIPointer(2, 3, GL_UNSIGNED_BYTE, 4, ctypes.c_void_p(1))
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)
        glVertexAttribDivisor(1, 1)
        glVertexAttribDivisor(2, 1)
        # print(f"Chunk data (MB): {self.chunk_data.nbytes / 1024 / 1024} MB")
        # print(f"Chunk mesh data (MB): {self.mesh_data.nbytes / 1024 / 1024} MB")
        
        return instance_vbo
    
    
    def bind_ivbo(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.ivbo)
        
        
    def unbind_ivbo(self):
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        
        
    def render(self):
        
        self.use_model_matrix()
        glBindBuffer(GL_ARRAY_BUFFER, self.ivbo)
        glDrawElementsInstanced(GL_TRIANGLES, len(indices), GL_UNSIGNED_BYTE, None, len(self.mesh_data))
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        
    
    def __del__(self):
        
        glDeleteBuffers(1, self.ivbo)
        print("Chunk deleted", self.chunk_position, end="\r")
    