# Architecture
# CollabSphere - Flask Clean Architecture REST API

Enterprise-grade REST API backend built with **Flask**, **SQLAlchemy**, **Marshmallow**, and **Clean Architecture (Onion Architecture)** principles.

---

## 🏛️ Kiến trúc dự án (Clean Architecture)

Hệ thống được thiết kế tuân thủ nghiêm ngặt nguyên lý Clean Architecture: các tầng phụ thuộc từ ngoài vào trong, tầng **Domain** là trung tâm và hoàn toàn độc lập với database hay web framework.

```text
Flask-CleanArchitecture-main/
├── src/
│   ├── api/                           # [Presentation Layer] Web API, Routing, Serialization
│   │   ├── controllers/               # Flask Blueprints & Route Handlers
│   │   │   ├── auth_controller.py     # Đăng ký, đăng nhập, JWT profile
│   │   │   ├── course_controller.py   # Quản lý khóa học (CRUD)
│   │   │   ├── todo_controller.py     # Quản lý công việc (CRUD)
│   │   │   └── user_controller.py     # Quản lý người dùng
│   │   ├── schemas/                   # Marshmallow Validation & Serialization Schemas
│   │   │   ├── course.py
│   │   │   ├── todo.py
│   │   │   └── user.py
│   │   ├── middleware.py              # JWT Auth Decorator, Request Logger, Global Error Handling
│   │   ├── responses.py               # Chuẩn hóa định dạng JSON Response
│   │   └── swagger.py                 # OpenAPI 3.0 / Swagger UI Specification
│   ├── domain/                        # [Domain Layer] Nghiệp vụ cốt lõi (Core Business)
│   │   ├── constants.py               # Constants toàn hệ thống
│   │   ├── exceptions.py              # Domain Exceptions (NotFound, Validation, Conflict, ...)
│   │   └── models/                    # Pure Domain Entities & Repository Interfaces
│   │       ├── course.py
│   │       ├── todo.py
│   │       ├── user.py
│   │       ├── icourse_repository.py
│   │       ├── itodo_repository.py
│   │       └── iuser_repository.py
│   ├── services/                      # [Application Layer / Use Cases] Business Logic
│   │   ├── auth_service.py            # Password hashing & JWT lifecycle
│   │   ├── course_service.py          # Nghiệp vụ khóa học
│   │   ├── todo_service.py            # Nghiệp vụ todo
│   │   └── user_service.py            # Nghiệp vụ quản lý user
│   ├── infrastructure/                # [Infrastructure Layer] Database, ORM, External Services
│   │   ├── databases/                 # Quản lý kết nối Database & Scoped Session
│   │   │   ├── base.py                # SQLAlchemy Base
│   │   │   ├── database.py            # Multi-DB Engine, Auto-fallback, Scoped Session
│   │   │   └── mssql.py               # SQL Server Adapter
│   │   ├── models/                    # SQLAlchemy ORM Models
│   │   │   ├── __init__.py            # Export toàn bộ ORM models
│   │   │   ├── user_model.py
│   │   │   ├── course_model.py
│   │   │   ├── todo_model.py
│   │   │   ├── appointment_model.py
│   │   │   ├── consultant_model.py
│   │   │   ├── course_register_model.py
│   │   │   ├── feedback_model.py
│   │   │   ├── program_model.py
│   │   │   └── survey_model.py
│   │   └── repositories/              # Triển khai Repository bằng SQLAlchemy
│   │       ├── course_repository.py
│   │       ├── todo_repository.py
│   │       └── user_repository.py
│   ├── app.py                         # Application Entry Point
│   ├── create_app.py                  # Application Factory
│   ├── config.py                      # Cấu hình môi trường đa Database
│   ├── cors.py                        # CORS Configuration
│   ├── dependency_container.py        # Dependency Injection Container
│   └── error_handler.py               # Exception Handler
├── tests/                             # Automated Test Suites (pytest)
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_courses.py
│   └── test_todos.py
├── Dockerfile                         # Container build
├── docker-compose.yml                 # Local stack deployment
├── requirements.txt                   # Danh sách thư viện Python
└── README.md
```

---

## 🚀 Các điểm nâng cấp nổi bật

1. **Hỗ trợ Đa Database & Tự động Fallback**:
   - Mặc định chạy ngay với **SQLite** (`sqlite:///default.db`) không cần cài đặt thêm phần mềm DB.
   - Hỗ trợ kết nối linh hoạt sang **Microsoft SQL Server**, **PostgreSQL**, hoặc **MySQL** qua biến môi trường `DATABASE_URI`.
   - Cơ chế tự động fallback về SQLite nếu cơ sở dữ liệu remote tạm thời chưa khả dụng.
2. **Thread-Safe Scoped Session**:
   - Sử dụng `scoped_session` và tự động dọn dẹp kết nối thông qua hook `@app.teardown_appcontext`, ngăn chặn triệt để tình trạng rò rỉ session và xung đột đa luồng.
3. **Hoàn thiện Tầng Domain & Clean Architecture**:
   - Tách biệt hoàn toàn Domain Entity khỏi SQLAlchemy ORM Models.
   - Bổ sung giao diện Repository (`ICourseRepository`, `ITodoRepository`, `IUserRepository`).
   - Xử lý lỗi tập trung thông qua Domain Exceptions (`NotFoundException`, `ValidationException`, `ConflictException`, `UnauthorizedException`).
4. **Bảo mật & Xác thực JWT**:
   - Mã hóa mật khẩu bảo mật chuẩn công nghiệp với `werkzeug.security` (PBKDF2/SHA256).
   - Xác thực token JWT (RFC 7519) và middleware decorator `@token_required` bảo vệ API.
5. **Hoàn thiện đầy đủ CRUD Controllers & Schemas**:
   - Viết lại toàn bộ `course_controller.py` với nghiệp vụ Course độc lập (trước đây bị copy đè từ Todo).
   - Bổ sung `auth_controller.py` và `user_controller.py`.
   - Validate dữ liệu đầu vào và serialize kết quả trả về bằng Marshmallow Schemas.
6. **Tài liệu API Tương tác Swagger UI**:
   - Tích hợp Swagger UI trực quan tại đường dẫn: `http://localhost:9999/docs`.
   - Hỗ trợ nhập JWT Bearer Token trực tiếp trên giao diện Swagger để test endpoint có bảo mật.
7. **Kiểm thử tự động (Automated Testing)**:
   - Bộ test suite toàn diện bằng `pytest` kiểm thử Auth, Courses, và Todos đạt 100% pass.
8. **Đóng gói Docker**:
   - Cung cấp sẵn `Dockerfile` và `docker-compose.yml` tối ưu hóa.

---

## 🛠️ Hướng dẫn cài đặt và chạy

### 1. Yêu cầu hệ thống
- Python 3.10 trở lên (đã test tương thích với Python 3.11, 3.12, 3.14).

### 2. Cài đặt môi trường ảo (Virtual Environment)

**Trên Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\activate.ps1
pip install -r requirements.txt
```

**Trên macOS / Linux:**
```bash
    ├── migrations
    ├── scripts
    │   └── run_postgres.sh
    ├── src
    │   ├── api
    │   │   ├── controllers
    │   │   │   └── ...  # controllers for the api
    │   │   ├── schemas
    │   │   │   └── ...  # Marshmallow schemas
    │   │   ├── middleware.py
    │   │   ├── responses.py
    │   │   └── requests.py
    │   ├── infrastructure
    │   │   ├── services
    │   │   │   └── ...  # Services that use third party libraries or services (e.g. email service)
    │   │   ├── databases
    │   │   │   └── ...  # Database adapaters and initialization
    │   │   ├── repositories
    │   │   │   └── ...  # Repositories for interacting with the databases
    │   │   └── models
    │   │   │   └── ...  # Database models
    │   ├── domain
    │   │   ├── constants.py
    │   │   ├── exceptions.py
    │   │   ├── models
    │   │   │   └── ...  # Business logic models
    │   ├── services
    │   │    └── ...  # Services for interacting with the domain (business logic)
    │   ├── app.py
    │   ├── config.py
    │   ├── cors.py
    │   ├── create_app.py
    │   ├── dependency_container.py
    │   ├── error_handler.py
    │   └── logging.py
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Domain Layer
### 3. Cấu hình biến môi trường (`.env`)
Tạo file `.env` tại thư mục gốc hoặc `src/.env` (tham khảo `.env.example`):
```env
FLASK_ENV=development
SECRET_KEY=collabsphere_super_secret_jwt_key_2026
JWT_SECRET_KEY=collabsphere_super_secret_jwt_key_2026

## Services Layer
# Mặc định sử dụng SQLite (chạy ngay, không cần cấu hình thêm):
DATABASE_URI=sqlite:///default.db

## Infrastructure Layer
# Hoặc nếu dùng MS SQL Server:
# DATABASE_URI=mssql+pymssql://sa:Aa%40123456@127.0.0.1:1433/FlaskApiDB
```

## Download source code (CMD)
    git clone https://github.com/ChienNguyensrdn/Flask-CleanArchitecture.git
## Kiểm tra đã cài python đã cài đặt trên máy chưa
    python --version
## Run app
### 4. Khởi chạy ứng dụng
```bash
python src/app.py
```
Ứng dụng sẽ chạy tại:
- **API Root**: `http://localhost:9999/`
- **Tài liệu Swagger UI**: `http://localhost:9999/docs`
- **OpenAPI Schema**: `http://localhost:9999/swagger.json`

 - Bước 1: Tạo môi trường ảo co Python (phiên bản 3.x)
     ## Windows:
     		py -m venv .venv
     ## Unix/MacOS:
     		python3 -m venv .venv
   - Bước 2: Kích hoạt môi trường:
     ## Windows:
     		.venv\Scripts\activate.ps1
     ### Nếu xảy ra lỗi active .venv trên winos run powshell -->Administrator
         Set-ExecutionPolicy RemoteSigned -Force
     ## Unix/MacOS:
     		source .venv/bin/activate
     
   - Bước 3: Cài đặt các thư viện cần thiết
     ## Install:
     pip install -r requirements.txt
     		
   - Bước 4: Chạy mã xử lý dữ liệu
     ## Run:
    		python app.py
---

## 🧪 Chạy Kiểm thử tự động (Unit & Integration Tests)

     Truy câp http://localhost:9999/docs
Chạy toàn bộ test suites với `pytest`:
```bash
pytest tests -v
```

---

## 🐳 Chạy với Docker

## Create file .env in folder /src/.env
    
    # Flask settings
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    
    # SQL Server settings
    DB_USER=sa
    DB_PASSWORD=Aa@123456
    DB_HOST=127.0.0.1
    DB_PORT=1433
    DB_NAME=FlaskApiDB
    
    
    DATABASE_URI = "mssql+pymssql://sa:Aa%40123456@127.0.0.1:1433/FlaskApiDB"
```bash
# Build và chạy với Docker Compose
docker-compose up --build -d

## pull image MS SQL server 
    
    ```bash
    docker pull mcr.microsoft.com/mssql/server:2025-latest
    ```
## Install MS SQL server in docker 
    ```bash
    docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=Aa123456" -p 1433:1433 --name sql1 --hostname sql1 -d  mcr.microsoft.com/mssql/server:2025-latest
    ```
## Test connect SQL server 
# Xem log
docker-compose logs -f
```

## ORM Flask (from sqlalchemy.orm )
Object Relational Mapping
---

Ánh xạ 1 class (OOP)  model src/infrastructure/models --> Table in database 
Ánh xạ các mối quan hệ (Relational) -- Khoá ngoại CSDL 
(n-n): many to many 
## 📋 Danh sách API Endpoints

| Method | Endpoint | Quyền hạn | Mô tả |
|---|---|---|---|
| `GET` | `/` | Public | Thông tin API & trạng thái |
| `GET` | `/docs` | Public | Giao diện Swagger UI |
| `POST` | `/auth/register` | Public | Đăng ký tài khoản mới & nhận JWT |
| `POST` | `/auth/login` | Public | Đăng nhập & lấy token JWT |
| `GET` | `/auth/me` | Bearer Token | Lấy thông tin tài khoản hiện tại |
| `GET` | `/users/` | Public | Lấy danh sách người dùng |
| `GET` | `/users/<id>` | Public | Lấy thông tin người dùng theo ID |
| `PUT` | `/users/<id>` | Bearer Token | Cập nhật thông tin người dùng |
| `DELETE` | `/users/<id>` | Bearer Token | Xóa tài khoản người dùng |
| `GET` | `/courses/` | Public | Lấy danh sách khóa học |
| `GET` | `/courses/<id>` | Public | Xem chi tiết khóa học |
| `POST` | `/courses/` | Public | Tạo mới khóa học |
| `PUT` | `/courses/<id>` | Public | Cập nhật khóa học |
| `DELETE` | `/courses/<id>` | Public | Xóa khóa học |
| `GET` | `/todos/` | Public | Lấy danh sách công việc |
| `GET` | `/todos/<id>` | Public | Xem chi tiết công việc |
| `POST` | `/todos/` | Public | Tạo mới công việc |
| `PUT` | `/todos/<id>` | Public | Cập nhật công việc |
| `DELETE` | `/todos/<id>` | Public | Xóa công việc |
