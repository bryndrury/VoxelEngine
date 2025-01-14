#version 330 core

// Vertex Attributes
layout (location = 0) in vec3 aPos;

// Instanced Attributes
layout (location = 1) in int aFaceNormalID;
layout (location = 2) in ivec3 aChunkPosition;

// Uniforms
uniform mat4 chunk_model; // Per Chunk basis
uniform mat4 view;
uniform mat4 projection;

// Output
flat out int ao_ID;
out vec2 uv;

const vec2 uv_coords[4] = vec2[4](
    vec2(0.0, 0.0), vec2(0.0, 1.0),
    vec2(1.0, 0.0), vec2(1.0, 1.0)
);

const int uv_indices[12] = int[12](
    3, 1, 0, 2, 1, 2,
    2, 1, 2, 3, 1, 0
);

mat4 rotateX(float angle) {
    float s = sin(angle);
    float c = cos(angle);
    return mat4(
        1.0, 0.0, 0.0, 0.0,
        0.0,   c,  -s, 0.0,
        0.0,   s,   c, 0.0,
        0.0, 0.0, 0.0, 1.0
    );
}

mat4 rotateY(float angle) {
    float s = sin(angle);
    float c = cos(angle);
    return 0.5 * mat4(
          c, 0.0,   s, 0.0,
        0.0, 1.0, 0.0, 0.0,
         -s, 0.0,   c, 0.0,
        0.0, 0.0, 0.0, 1.0
    );
}

mat4 rotateZ(float angle) {
    float s = sin(angle);
    float c = cos(angle);
    return mat4(
          c,  -s, 0.0, 0.0,
          s,   c, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0
    );
}

mat4 getFaceRotationMatrix(int normal_id) {
    // Rotation matrix for each face
    // 0: Top // 1: Bottom // 2: Left // 3: Right // 4: Front // 5: Back  (else)
    mat4 rotationMatrix = mat4(1.0);
    float PI = radians(180.0);
    if (normal_id == 0) {                   // Top
        rotationMatrix = rotateX(PI/2.0);
    } else if (normal_id == 1) {            // Bottom
        rotationMatrix = rotateX(-PI/2.0);
        rotationMatrix *= rotateZ(PI);
    } else if (normal_id == 2) {            // Left
        rotationMatrix = rotateY(PI/2.0);
    } else if (normal_id == 3) {            // Right
        rotationMatrix = rotateY(-PI/2.0);
    } else if (normal_id == 4) {            // Front
        rotationMatrix = rotateX(PI);
        rotationMatrix *= rotateZ(PI);
    } else {                                // Back
        rotationMatrix = rotateX(2*PI);
    }

    return rotationMatrix;
}

void main()
{
    int uv_index = gl_VertexID % 6 + (aFaceNormalID % 1) * 6;
    uv = uv_coords[uv_indices[uv_index]];

    mat4 faceRotationMat = getFaceRotationMatrix(aFaceNormalID);
    ao_ID = aFaceNormalID;

    mat4 model = mat4(
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        aChunkPosition.x, aChunkPosition.y, aChunkPosition.z, 1.0
    );
    
    gl_Position = projection * view * chunk_model * model * faceRotationMat * vec4(aPos, 1.0);
}