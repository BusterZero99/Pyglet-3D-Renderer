VERT_SRC = """
#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;
layout(location = 2) in vec2 texcoord;

uniform mat4 mvp;

out vec3 fragNormal;
out vec3 fragPos;

void main() {
    gl_Position = mvp * vec4(position, 1.0);
    fragNormal = normal;
    fragPos = position;
}
"""

FRAG_SRC = """
#version 330 core
in vec3 fragNormal;
in vec3 fragPos;
uniform float time;
out vec4 FragColor;

vec3 rainbow(float t) {
    float r = abs(t * 6.0 - 3.0) - 1.0;
    float g = 2.0 - abs(t * 6.0 - 2.0);
    float b = 2.0 - abs(t * 6.0 - 4.0);
    return clamp(vec3(r, g, b), 0.0, 1.0);
}

void main() {
    float t = fract((fragPos.x + fragPos.y + fragPos.z) * 0.1 + time * 0.2);
    vec3 color = rainbow(t);
    vec3 lightDir = normalize(vec3(0.5, 1.0, 0.3));
    float diff = max(dot(normalize(fragNormal), lightDir), 0.0);
    FragColor = vec4(color * diff, 1.0);
}
"""