#version 330 core
 
// Input from vertex shader
flat in int ao_ID;
in vec2 uv;

// Input from uniform
uniform sampler2D tex;

// Output
out vec4 FragColor;

// 'Ambient Occlusion' shading
float faceColor(int normal_id) {
    if (normal_id == 0) { // Top
        return 1.0;
    }
    if (normal_id == 1) { // Bottom 
        return 0.2;
    }
    if (normal_id == 2) { // Left
        return 0.6;
    }
    if (normal_id == 3) { // Right
        return 0.4;
    }
    if (normal_id == 4) { // Front
        return 0.3;
    }
    if (normal_id == 5) { // Back
        return 0.8;
    }
    return 0.0;
}

vec2 getTextCoord(int normal_id, vec2 uv) {
    int testing = 0;
    if (testing == 1) {
        return uv;
    }

    int textureID = 0;
    vec2 uv_coords = uv;
    if (normal_id == 0) { // Top
        uv_coords = vec2(uv.x/3 - (1.0/3.0), uv.y/2.0 + (textureID/2.0));
        return uv_coords;
    }
    if (normal_id == 1) { // Bottom
        uv_coords = vec2(uv.x/3, uv.y/2.0 + (textureID/2.0));
        return uv_coords;
    }
    if (normal_id == 2 || normal_id == 3 || normal_id == 4 || normal_id == 5) { // Sides
        uv_coords = vec2(uv.x/3 - (2.0/3.0), uv.y/2.0 + (textureID/2.0));
        return uv_coords;
    }
    return uv_coords;
}

void main()
{
    vec2 uv_coords = getTextCoord(ao_ID, uv);
    vec3 tex_col = texture(tex, uv_coords).rgb;
    FragColor = vec4(tex_col, 1.0) * faceColor(ao_ID);
}