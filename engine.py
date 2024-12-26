from settings import *
from texture import Texture
from camera import Camera
from world import World
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
        self.setup_world()
        
    def initialise_attributes(self):
        self.world = None
        self.camera = Camera(pos=PLAYER_POS, front=PLAYER_DIR)
        self.clock = pg.time.Clock()
        
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)
        self.texture = Texture("test.png")
        
        self.running = True
        self.frame_start = 0
        
    def setup_pygame(self):
        pg.init()
        
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, 1)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)
        # Anti-aliasing
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLEBUFFERS, 1)
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, 16)
        pg.display.gl_set_attribute(pg.GL_ACCELERATED_VISUAL, 1)
        
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        pg.mouse.set_pos((400, 300))
        pg.display.set_caption("Voxel Engine")
    
        self.screen = pg.display.set_mode(SCREEN_SIZE, pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE, 1)
                     
    def setup_OpenGL(self):
        glClearColor(178.0/255.0, 223.0/255, 237.0/255.0, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        # Anti-aliasing
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_FASTEST)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_FASTEST)
    
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
        self.world = World(self.chunkShaderProgram)
        
    def handle_events(self):
        
        self.frame_start = pg.time.get_ticks()
        
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
        
        # modelLoc = glGetUniformLocation(self.chunkShaderProgram, "model")
        viewLoc = glGetUniformLocation(self.chunkShaderProgram, "view")
        projLoc = glGetUniformLocation(self.chunkShaderProgram, "projection")
        
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(projLoc, 1, GL_FALSE, glm.value_ptr(projection))
        
        CPU_time = pg.time.get_ticks() - self.frame_start
        
        glBindVertexArray(self.vao)
        
        self.world.render(view, projection)
        
        pg.display.flip()
        
        pg.display.set_caption(f"Voxel Engine | CPU time: {CPU_time} ms | GPU time: {pg.time.get_ticks() - self.frame_start - CPU_time} ms | FPS: {self.clock.get_fps() :.0f}")
        
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
        
        while self.running:
            
            self.handle_events()
            self.render()
            pg.time.wait(30)
        
        self.shutdown()
        
    def panik(self, message):
        # In case of emergency, break glass
        print(message)
        pg.quit()
        gc.collect()
        sys.exit()