from settings import *
from chunk import Chunk
from texture import Texture
from camera import Camera
import sys
import gc

class Engine():
    
    def __init__(self):
        self.on_init()
        
    def on_init(self):
        self.setup_pygame()
        self.setup_OpenGL()
        self.initialise_attributes()
        self.setup_chunk_buffers()
        self.setup_chunk_shader()
        
    def initialise_attributes(self):
        self.camera = Camera(pos=PLAYER_POS)
        self.clock = pg.time.Clock()
        
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)
        self.texture = Texture("texture.png")
        
        self.running = True
        self.frame_start = 0
        
    def setup_pygame(self):
        pg.init()
        
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, 1)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)
        
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        pg.mouse.set_pos((400, 300))
        pg.display.set_caption("Voxel Engine")
    
        self.screen = pg.display.set_mode(SCREEN_SIZE, pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
                     
    def setup_OpenGL(self):
        glClearColor(178.0/255.0, 223.0/255, 237.0/255.0, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glEnable(GL_MULTISAMPLE)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    def setup_chunk_buffers(self):
            
        # Vertex attributes
        glBindVertexArray(self.vao)
        
        # Setup vertex buffer
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        # Setup element buffer
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        
    def setup_chunk_shader(self):
        # Create shader program
        with open("shaders/cube.vert", "r") as file:
            vertex_source = file.read()
        with open("shaders/cube.frag", "r") as file:
            fragment_source = file.read()

        shaderProgram = compileProgram(
            compileShader(vertex_source, GL_VERTEX_SHADER),
            compileShader(fragment_source, GL_FRAGMENT_SHADER)
        )
        
        if not glGetProgramiv(shaderProgram, GL_LINK_STATUS):
            print("Program linking failed:")
            print(glGetProgramInfoLog(progshaderProgramram).decode())
        
        glUseProgram(shaderProgram)
        
        # Use textures
        self.texture.use_texture(shaderProgram)
        glUniform1i(glGetUniformLocation(shaderProgram, "texture1"), 0)
        
        self.chunkShaderProgram = shaderProgram
        
    def setup_world(self):
        self.chunks = [None for _ in range(WORLD_VOLUME)]
        for wx in range(WORLD_WIDTH):
            for wz in range(WORLD_HEIGHT):
                for wy in range(WORLD_DEPTH):
                    self.chunks[wx + wz * WORLD_WIDTH + wy * WORLD_WIDTH * WORLD_HEIGHT] = Chunk(shaderProgram=self.chunkShaderProgram,pos=(wx * CHUNK_SIZE, wy * CHUNK_SIZE, wz * CHUNK_SIZE))
        
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.MOUSEMOTION:
                self.camera.process_mouse(event.pos[0], event.pos[1])
            
        self.camera.process_keyboard(pg.key.get_pressed(), self.clock.get_time())
             
    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
        view = self.camera.get_view_matrix()
        projection = glm.perspective(glm.radians(PLAYER_FOV), ASP_RATIO, NEAR, FAR)
        
        # modelLoc = glGetUniformLocation(shaderProgram, "model")
        viewLoc = glGetUniformLocation(self.chunkShaderProgram, "view")
        projLoc = glGetUniformLocation(self.chunkShaderProgram, "projection")
        
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(projLoc, 1, GL_FALSE, glm.value_ptr(projection))
        
        CPU_time = pg.time.get_ticks() - self.frame_start
        
        glBindVertexArray(self.vao)
        
        for chunk in self.chunks:
            if chunk is not None:
                chunk.render()
        
        pg.display.flip()
        
        pg.display.set_caption(f"Voxel Engine | CPU time: {CPU_time} ms | GPU time: {pg.time.get_ticks() - self.frame_start - CPU_time} ms | FPS: {self.clock.get_fps() :.0f}")
        
        # pg.time.wait(5)
        self.clock.tick()
        
    def shutdown(self):
        self.running = False
        
        glDeleteVertexArrays(1, self.vao)
        glDeleteBuffers(1, self.vbo)
        glDeleteBuffers(1, self.ebo)
        glDeleteProgram(self.chunkShaderProgram)
        
        pg.quit()
        gc.collect()
        print("Program terminated successfully.")
        
    def run(self):
        self.setup_world()
        
        while self.running:
            self.frame_start = pg.time.get_ticks()
            
            self.handle_events()
            self.render()
        
        self.shutdown()
        
    def panik(self, message):
        # In case of emergency, break glass
        print(message)
        pg.quit()
        gc.collect()
        sys.exit()