#version 330 core

// Input
flat in int ao_ID;

// Output
out vec4 FragColor;

float faceColor(int normal_id) {
    if (normal_id == 0) { // Top
        return 1.0;
    }
    if (normal_id == 1) { // Bottom 
        return 0.1;
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

void main()
{
    FragColor = faceColor(ao_ID) * vec4(1.0, 1.0, 1.0, 1.0);
}