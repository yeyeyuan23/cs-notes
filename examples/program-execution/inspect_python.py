"""Show compilation and execution as separate operations."""
import dis

source = """
def add(a, b):
    return a + b

print(add(2, 3))
"""

print("1. 开始编译")
code = compile(source, "<example>", "exec")
print("2. 编译结束；source 内的 print 尚未执行")

print("3. 查看字节码")
dis.dis(code)

print("4. 开始执行 source")
exec(code, {})
