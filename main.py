from settings import *

from camera import Camera
from chunk import Chunk
# from world import World
from texture import Texture

if __name__ == "__main__":
    
    
    pg.init()
    
    pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
    pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
    pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
    pg.display.gl_set_attribute(pg.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, 1)
    pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)
    
    screen = pg.display.set_mode(SCREEN_SIZE, pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
    pg.display.set_caption("Voxel Engine")
     
    camera = Camera(pos=PLAYER_POS)
    pg.event.set_grab(True)
    pg.mouse.set_visible(False)
    pg.event.set_grab(True)
    pg.mouse.set_pos((400, 300))
    
    glClearColor(178.0/255.0, 223.0/255, 237.0/255.0, 1)
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glEnable(GL_MULTISAMPLE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    chunk = Chunk()
    texture = Texture()
    
    vertices = np.array([
        [-0.5, -0.5, 0.5,],
        [0.5, -0.5, 0.5,],
        [0.5, 0.5, 0.5,],
        [-0.5, 0.5, 0.5,],
    ], dtype=np.float32)
    indices = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint8)
    
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    ebo = glGenBuffers(1)
    instance_vbo = glGenBuffers(1)
    
    # Vertex attributes
    glBindVertexArray(vao)
    
    # Setup vertex buffer
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, instance_vbo)
    glBufferData(GL_ARRAY_BUFFER, chunk.mesh_data.nbytes, chunk.mesh_data, GL_STATIC_DRAW)
    glVertexAttribIPointer(1, 4, GL_UNSIGNED_BYTE, 4, ctypes.c_void_p(0))
    glVertexAttribIPointer(2, 3, GL_UNSIGNED_BYTE, 4, ctypes.c_void_p(1))
    glEnableVertexAttribArray(1)
    glEnableVertexAttribArray(2)
    glVertexAttribDivisor(1, 1)
    glVertexAttribDivisor(2, 1)
    print(f"Chunk data (MB): {chunk.chunk_data.nbytes / 1024 / 1024} MB")
    print(f"Chunk mesh data (MB): {chunk.mesh_data.nbytes / 1024 / 1024} MB")
    
    # Setup element buffer
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
    
    # Create shader program
    with open("shaders/cube.vert", "r") as file:
        vertex_source = file.read()
    with open("shaders/cube.frag", "r") as file:
        fragment_source = file.read()
        
    shaderProgram = compileProgram(
        compileShader(vertex_source, GL_VERTEX_SHADER),
        compileShader(fragment_source, GL_FRAGMENT_SHADER)
    )
    glUseProgram(shaderProgram)
    
    # Use textures
    texture.use_texture(shaderProgram)
    glUniform1i(glGetUniformLocation(shaderProgram, "texture1"), 0)
    
    
    if not glGetProgramiv(shaderProgram, GL_LINK_STATUS):
        print("Program linking failed:")
        print(glGetProgramInfoLog(progshaderProgramram).decode())
    
    clock = pg.time.Clock()
    running = True
    
    while running:
        frame_start = pg.time.get_ticks()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEMOTION:
                camera.process_mouse(event.pos[0], event.pos[1])
            
        camera.process_keyboard(pg.key.get_pressed(), clock.get_time())
                
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        view = camera.get_view_matrix()
        projection = glm.perspective(glm.radians(PLAYER_FOV), ASP_RATIO, NEAR, FAR)
        
        # modelLoc = glGetUniformLocation(shaderProgram, "model")
        viewLoc = glGetUniformLocation(shaderProgram, "view")
        projLoc = glGetUniformLocation(shaderProgram, "projection")
        
        CPU_time = pg.time.get_ticks() - frame_start
        
        # glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm.value_ptr(model))
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(projLoc, 1, GL_FALSE, glm.value_ptr(projection))
        
        glBindVertexArray(vao)
        glDrawElementsInstanced(GL_TRIANGLES, len(indices), GL_UNSIGNED_BYTE, None, len(chunk.mesh_data))
        
        pg.display.flip()
        
        pg.display.set_caption(f"Voxel Engine | CPU time: {CPU_time} ms | GPU time: {pg.time.get_ticks() - frame_start - CPU_time} ms | FPS: {clock.get_fps() :.0f}")
        
        pg.time.wait(5)
        clock.tick()
    
    pg.quit()
    
    glDeleteVertexArrays(1, vao)
    glDeleteBuffers(1, vbo)
    glDeleteBuffers(1, ebo)
    glDeleteBuffers(1, instance_vbo)
    glDeleteProgram(shaderProgram)
    
    print("Program terminated successfully.")
    