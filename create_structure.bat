@echo off

REM Root directory
@REM set ROOT=log_pattern_detection_tool
set ROOT=.

REM Create directories if they do not exist
call :create_folder "%ROOT%"
call :create_folder "%ROOT%\concurrency"
call :create_folder "%ROOT%\config"
call :create_folder "%ROOT%\docs"
call :create_folder "%ROOT%\examples"
call :create_folder "%ROOT%\limiter"
call :create_folder "%ROOT%\logs"
call :create_folder "%ROOT%\middleware"
call :create_folder "%ROOT%\observability"
call :create_folder "%ROOT%\protocol"
call :create_folder "%ROOT%\state"
call :create_folder "%ROOT%\tests"
call :create_folder "%ROOT%\utils"
call :create_folder "%ROOT%\tests\integration"
call :create_folder "%ROOT%\tests\load"
call :create_folder "%ROOT%\tests\unit"

REM Create files only if they do not exist
REM Python source files (with header)
call :create_py_file "%ROOT%\main.py"
call :create_py_file "%ROOT%\setup.py"

call :create_py_file "%ROOT%\concurrency\__init__.py"
call :create_py_file "%ROOT%\concurrency\clock.py"
call :create_py_file "%ROOT%\concurrency\locks.py"

call :create_py_file "%ROOT%\config\__init__.py"
call :create_py_file "%ROOT%\config\constants.py"
call :create_py_file "%ROOT%\config\settings.py"

call :create_py_file "%ROOT%\examples\__init__.py"
call :create_py_file "%ROOT%\examples\leaky_bucket_basic.py"
call :create_py_file "%ROOT%\examples\middleware_example.py"
call :create_py_file "%ROOT%\examples\token_bucket_basic.py"

call :create_py_file "%ROOT%\limiter\__init__.py"
call :create_py_file "%ROOT%\limiter\base.py"
call :create_py_file "%ROOT%\limiter\leaky_bucket.py"
call :create_py_file "%ROOT%\limiter\manager.py"
call :create_py_file "%ROOT%\limiter\token_bucket.py"

call :create_py_file "%ROOT%\middleware\__init__.py"
call :create_py_file "%ROOT%\middleware\api_middleware.py"

call :create_py_file "%ROOT%\observability\__init__.py"
call :create_py_file "%ROOT%\observability\logger.py"
call :create_py_file "%ROOT%\observability\metrics.py"

call :create_py_file "%ROOT%\protocol\__init__.py"
call :create_py_file "%ROOT%\protocol\request.py"
call :create_py_file "%ROOT%\protocol\response.py"

call :create_py_file "%ROOT%\state\__init__.py"
call :create_py_file "%ROOT%\state\bucket.py"
call :create_py_file "%ROOT%\state\memory_store.py"
call :create_py_file "%ROOT%\state\repository.py"

call :create_py_file "%ROOT%\utils\__init__.py"
call :create_py_file "%ROOT%\utils\identifiers.py"

call :create_py_file "%ROOT%\tests\integration\test_middleware_flow.py"
call :create_py_file "%ROOT%\tests\integration\test_multi_client_limits.py"
call :create_py_file "%ROOT%\tests\load\test_high_throughput.py"
call :create_py_file "%ROOT%\tests\unit\test_concurrency.py"
call :create_py_file "%ROOT%\tests\unit\test_leaky_bucket.py"
call :create_py_file "%ROOT%\tests\unit\test_repository.py"
call :create_py_file "%ROOT%\tests\unit\test_token_bucket.py"

REM Non-Python files (empty)
call :create_file "%ROOT%\docs\api.md"

call :create_file "%ROOT%\examples\distributed_mode_note.md"

call :create_file "%ROOT%\logs\api_rate_limiter.log"

call :create_file "%ROOT%\requirements.txt"
call :create_file "%ROOT%\README.md"
call :create_file "%ROOT%\LICENSE"

echo Folder structure created (existing files and folders were preserved).
goto :eof

REM -------------------------------------------
REM Create folders if does not exist
REM -------------------------------------------

:create_folder
if not exist "%~1" (
    mkdir "%~1"
)

REM -------------------------------------------
REM Create empty file if it does not exist
REM -------------------------------------------

:create_file
if not exist "%~1" (
    type nul > "%~1"
)

exit /b

REM -------------------------------------------
REM Create python file with GPL header
REM -------------------------------------------
:create_py_file
if exist "%~1" exit /b

set FILEPATH=%~1
set FILENAME=%~n1

(
echo # --------------------------------------------------
echo # -*- Python -*- Compatibility Header
echo #
echo # Copyright ^(C^) 2023 Developer Jarvis ^(Pen Name^)
echo #
echo # This file is part of the API Rate Limiter Library. This library is free
echo # software; you can redistribute it and/or modify it under the
echo # terms of the GNU General Public License as published by the
echo # Free Software Foundation; either version 3, or ^(at your option^)
echo # any later version.
echo #
echo # This program is distributed in the hope that it will be useful,
echo # but WITHOUT ANY WARRANTY; without even the implied warranty of
echo # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
echo # GNU General Public License for more details.
echo #
echo # You should have received a copy of the GNU General Public License
echo # along with this program. If not, see ^<https://www.gnu.org/licenses/^>.
echo #
echo # SPDX-License-Identifier: GPL-3.0-or-later
echo #
echo # API Rate Limiter - Implement token-bucket or leaky-bucket algorithm
echo #           Skills: algorithms, concurrency, API design
echo #
echo # Author: Developer Jarvis ^(Pen Name^)
echo # Contact: https://github.com/DeveloperJarvis
echo #
echo # --------------------------------------------------
echo.
echo # --------------------------------------------------
echo # %FILENAME%% MODULE
echo # --------------------------------------------------
echo.
echo # --------------------------------------------------
echo # imports
echo # --------------------------------------------------
echo.
) > "%FILEPATH%"

exit /b