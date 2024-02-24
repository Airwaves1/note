# Uniform
- 在Shader执行运算的时候，彼此之间都是数据不共享的，但是指令一致
- 被当前Shader运行的所有运算单元共享的变量，成为Uniform变量

# Uniform 变量语法

- GLSL中，使用uniform关键字声明一个Uniform变量
```glsl
uniform vec3 direction;
uniform float time;

void main() {
    direction = direction * 2.0f;
    time = time + 1.0f;
}
```

- 设置Shader当中的Uniform变量
```c
//获取Uniform变量在Shader中的位置
GLuint location = glGetUniformLocation(program, "time");
//为location对应的Uniform变量赋值
glUniform1f(location, 0.5f);
```
```c
//获取Uniform变量在Shader中的位置
GLuint location = glGetUniformLocation(program, "direction");
//为location对应的Uniform变量赋值
glUniform3f(location, 0.5f, 1.0f, 0.8f);
```


线性映射公式
`newValue = (oldValue * (maxNew - minNew)) + minNew`
- newValue: 新的值
- oldValue: 旧的值
- maxNew: 新的最大值
- minNew: 新的最小值


#移动中变换颜色的三角形
```c
#version 460 core
layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aColor;

uniform float time;

out vec3 ourColor;

void main()
{
	gl_Position = vec4(aPos.x+sin(2.0*time)/2.0,aPos.yz, 1.0);
	ourColor = aColor;
	ourColor = aColor*(cos(time)+1.0f)/2.0f;
}
```

```c
#version 460 core
out vec4 FragColor;

uniform float time;

in vec3 ourColor;

void main()
{
	float intensity = (sin(time)+1.0f)/2.0f;
	FragColor = vec4(vec3(intensity) + ourColor, 1.0f);
}
```

```c
void Shader::setFloat(const std::string& name, float value) const
{
	//1.通过名称拿到Uniform变量的位置Location
	GLuint location = GL_CALL(glGetUniformLocation(m_shaderProgram, name.c_str()));

	//2.通过Location设置Uniform变量的值
	GL_CALL(glUniform1f(location, value));
}

void render()
{
	//先清空颜色缓冲
	GL_CALL(glClear(GL_COLOR_BUFFER_BIT));

	//绑定Shader程序
	shader->begin();

	shader->setFloat("time", (float)glfwGetTime());

	//绑定vao
	GL_CALL(glBindVertexArray(vao));
	//发出绘制指令
	GL_CALL(glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, 0));

	//解绑vao	
	GL_CALL(glBindVertexArray(0));
	//解绑Shader程序
	shader->end();
}