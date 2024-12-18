from settings import *

from camera import Camera

if __name__ == "__main__":
    
    pg.init()
    
    pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
    pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
    pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
    pg.display.gl_set_attribute(pg.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, 1)
    pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)
    
    screen = pg.display.set_mode((800, 600), pg.OPENGL | pg.DOUBLEBUF)
    pg.display.set_caption("Voxel Engine")
    
    camera = Camera()
    pg.event.set_grab(True)
    pg.mouse.set_visible(False)
    pg.event.set_grab(True)
    pg.mouse.set_pos((400, 300))
    
    glClearColor(0.2, 0.2, 0.2, 1)
    
    glEnable(GL_DEPTH_TEST)
    
    TOP_FACE = np.array([
        [-0.5, -0.5, 0.5,],
        [0.5, -0.5, 0.5,],
        [0.5, 0.5, 0.5,],
        [-0.5, 0.5, 0.5,],
    ], dtype=np.float32)
    TOP_FACE_EBO = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)
    
    vertices = TOP_FACE
    indices = TOP_FACE_EBO
    
    face_instances = np.array([0, 1, 2, 3, 4, 5], dtype=np.uint8) # To indicate which faces to render
    
    
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
    
    # Setup instance buffer
    glBindBuffer(GL_ARRAY_BUFFER, instance_vbo)
    glBufferData(GL_ARRAY_BUFFER, face_instances.nbytes, face_instances, GL_STATIC_DRAW)
    glVertexAttribIPointer(1, 1, GL_UNSIGNED_BYTE, 0, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)
    glVertexAttribDivisor(1, 1)
    
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
    
    
    if not glGetProgramiv(shaderProgram, GL_LINK_STATUS):
        print("Program linking failed:")
        print(glGetProgramInfoLog(progshaderProgramram).decode())
        
    # Uniforms
    model = glm.mat4(1.0)
    projection = glm.perspective(glm.radians(45.0), 800/600, 0.1, 100.0)
    view = glm.mat4(1.0)
    
    clock = pg.time.Clock()
    running = True
    
    while running:
        pg.display.set_caption(f"Voxel Engine | FPS: {clock.get_fps() :.0f}")
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEMOTION:
                camera.process_mouse(event.pos[0], event.pos[1])
                
        camera.process_keyboard(pg.key.get_pressed(), clock.get_time())
                
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        view = camera.get_view_matrix()
        
        modelLoc = glGetUniformLocation(shaderProgram, "model")
        viewLoc = glGetUniformLocation(shaderProgram, "view")
        projLoc = glGetUniformLocation(shaderProgram, "projection")
        
        glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm.value_ptr(model))
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(projLoc, 1, GL_FALSE, glm.value_ptr(projection))
        
        glBindVertexArray(vao)
        glDrawElementsInstanced(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None, len(face_instances))
        
        pg.display.flip()
        pg.time.wait(3)
        clock.tick()
    
    pg.quit()
    
    glDeleteVertexArrays(1, vao)
    glDeleteBuffers(1, vbo)
    glDeleteBuffers(1, ebo)
    glDeleteBuffers(1, instance_vbo)
    glDeleteProgram(shaderProgram)
    
    print("Program terminated successfully.")
    