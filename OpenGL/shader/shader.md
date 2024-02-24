# 1. 什么是 Shader
- Shader 是一种运行在 GPU 上的程序，它可以控制图形的渲染过程。Shader 是一种非常灵活的编程方式，可以用来实现各种各样的效果，比如光照、阴影、材质、动画等等。
- Shader对三角形数据的处理，分为两个阶段：顶点着色器和片段着色器，**Vertex Shader** 和 **Fragment Shader**。


# 2. GLSL 语言（Graphics Library Shading Language）
- GLSL 是一种专门为图形编程设计的编程语言，它是一种 C 语言的变种，专门用来编写 Shader，它包含一些针对向量矩阵运算的特殊语法。
- 特点
    - 将输入转换为输出的程序
    - 非常独立，彼此间无法进行通信，只能通过输入和输出相互承接


# 3. Vertex Shader
- 顶点着色器是 Shader 的第一个阶段，它的主要任务是对顶点坐标进行处理，将顶点坐标转换为屏幕坐标。
- 顶点着色器的输入是顶点数据，输出是顶点坐标。

```c
#version 460 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;

void main()
{
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
```

- `#version 460 core`：指定了 GLSL 的版本号，这里是 4.6 版本。

- 理解layout
    - 它是从输入变量中提取数据的位置，在VAO中，我们通过glVertexAttribPointer函数指定了顶点属性的位置，这里的layout就是指定了输入变量的位置。
    - `layout (location = 0) in vec3 aPos;`：指定了输入变量 aPos 的位置，这里是 0。
    - `layout (location = 1) in vec3 aColor;`：指定了输入变量 aColor 的位置，这里是 1。

    - `in vec3 aPos;`：输入变量 aPos，它是一个 vec3 类型的变量，表示顶点的位置。
    - `in vec3 aColor;`：输入变量 aColor，它是一个 vec3 类型的变量，表示顶点的颜色。

- 理解gl_Position
    - 一般默认输入的坐标为NDC坐标，即归一化设备坐标，范围为[-1, 1]，具体情况要看具体的坐标系进行转换。
    - `gl_Position`：是一个内建输出变量，它表示顶点的位置，是一个 vec4 类型的变量，表示齐次坐标。
    - 它负责将输入变量 aPos 的 x、y、z 分量转换为屏幕坐标，向后续阶段输出顶点位置处理结果。
    - `vec4(aPos.x, aPos.y, aPos.z, 1.0)`：将输入变量 aPos 的 x、y、z 分量赋值给 gl_Position 的 x、y、z 分量，w 分量赋值为 1.0。

# 4. Fragment Shader
- 片段着色器是 Shader 的第二个阶段，它的主要任务是确定像素的最终颜色。
- 片段着色器的输入是顶点着色器的输出，输出是片段颜色。

```c
#version 460 core
out vec4 FragColor;

void main()
{
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
}
```

- `out vec4 FragColor;`：输出变量 FragColor，它是一个 vec4 类型的变量，表示片段的颜色。

- `FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);`：将颜色值赋值给输出变量 FragColor，这里是橙色。


# 5. Shader 程序的编译
- Shader作为GPU端运行的程序，也需要编译和链接，这里我们使用GLSL语言，需要使用OpenGL提供的API进行编译和链接。

- 编译 Shader 程序
    - 创建一个 Shader 对象
    - 将 Shader 源码附加到 Shader 对象上
    - 编译 Shader 对象
    - 检查编译错误

```c

void prepareShader()
{
//1.准备顶点着色器与片段着色器
	const char* vertexShaderSource = R"(
		#version 460 core
		layout(location = 0) in vec3 aPos;
		layout(location = 1) in vec3 aColor;

		out vec3 ourColor;

		void main()
		{
			gl_Position = vec4(aPos, 1.0);
			ourColor = aColor;
		}
	)";

	const char* fragmentShaderSource = R"(
		#version 460 core
		out vec4 FragColor;

		in vec3 ourColor;

		void main()
		{
			FragColor = vec4(ourColor, 1.0);
		}
	)";


//2.创建Shader程序
	GLuint vertexShader, fragmentShader;
	vertexShader = glCreateShader(GL_VERTEX_SHADER);
	fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);

//3. 为Shader程序输入Shader代码
	GL_CALL(glShaderSource(vertexShader, 1, &vertexShaderSource, NULL));
	GL_CALL(glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL));

//4. 查看是否正确编译
	int success = 0;

	GL_CALL(glCompileShader(vertexShader));
	//检查vertex编译结果
	glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);

	if (!success)
	{
		char infoLog[512];
		glGetShaderInfoLog(vertexShader, 512, NULL, infoLog);	//获取错误信息
		std::cout << "ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" << infoLog << std::endl;
	}

	GL_CALL(glCompileShader(fragmentShader));
	//检查fragment编译结果
	glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, &success);

	if (!success)
	{
		char infoLog[512];
		glGetShaderInfoLog(fragmentShader, 512, NULL, infoLog);
		std::cout << "ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n" << infoLog << std::endl;
	}

//5. 创建一个Program壳子
	GLuint shaderProgram = glCreateProgram();

//6. 将vs和fs附加到Program上
	GL_CALL(glAttachShader(shaderProgram, vertexShader));
	GL_CALL(glAttachShader(shaderProgram, fragmentShader));

//7. 执行Program，形成最终的Shader程序
	GL_CALL(glLinkProgram(shaderProgram));
	//检查链接结果
	glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);
	if (!success)
	{
		char infoLog[512];
		glGetProgramInfoLog(shaderProgram, 512, NULL, infoLog);
		std::cout << "ERROR::SHADER::PROGRAM::LINK_FAILED\n" << infoLog << std::endl;
	}

//8. 清理，删除vs和fs
	GL_CALL(glDeleteShader(vertexShader));
	GL_CALL(glDeleteShader(fragmentShader));

}

```
