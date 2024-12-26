from settings import *

class Chunk():
    
    def __init__(self, shaderProgram, pos=(0,0,0)):
        self.shaderProgram = shaderProgram
        self.chunk_position = pos
        
        # Set in the world class:
        self.chunk_data = None
        self.chunk_mesh = None
    
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
    