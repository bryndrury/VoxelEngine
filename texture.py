from settings import *

class Texture():
    
    def __init__(self):
        self.image = None
        self.texture = self.generate_texture("test.png")
        
    def generate_texture(self, filename):
        
        image = pg.image.load(f"assets/{filename}")
        image = pg.transform.flip(image, flip_x=True, flip_y=False)
        self.image = image
        image_data = pg.image.tostring(image, 'RGBA', False)
        
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(), image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)

        return self.texture
    
    def use_texture(self, shader):
        glBindTexture(GL_TEXTURE_2D, self.texture)
        
    def unbind_texture(self):
        glBindTexture(GL_TEXTURE_2D, 0)
        
        
    def delete_texture(self):
        glDeleteTextures(1, self.texture)
        
    def __del__(self):
        self.delete_texture()
        
        
        