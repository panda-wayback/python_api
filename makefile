# 安装依赖
install-deps:
	pip install -r requirements.txt

# 安装项目为可编辑模式（开发环境，用于导入路径优化）
install:
	pip install -r requirements.txt
	pip install -e .

# 运行 FastAPI 应用（使用优化后的导入路径）
run:
	uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload

# 一个方便的 push 命令
# 包含所有 需要提交的文件
# 使用方法: make push
commit:
	git add .
	git add -u
	git add -A
	git commit -m "update"

push-current:
	git add .
	git add -u
	git add -A
	git commit -m "update"
	git push origin $(shell git branch --show-current)

# 合并所有 commit 到一个
# 使用方法: make squash
squash:
	@echo "开始合并所有 commit..."
	@echo "1. 获取第一个 commit 的 hash..."
	@FIRST_COMMIT=$$(git rev-list --max-parents=0 HEAD) && \
	echo "2. 重置到第一个 commit，但保留所有文件变更..." && \
	git reset --soft $$FIRST_COMMIT && \
	echo "3. 创建新的合并 commit..." && \
	git commit -m "合并所有 commit" && \
	echo "合并完成！"

# 打包命令 pyinstaller
build2:
	rm -rf build/ dist/ *.spec
	pyinstaller --onefile src/main.py
	@echo "构建完成!"