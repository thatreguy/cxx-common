set(VCPKG_TARGET_ARCHITECTURE arm64)
set(VCPKG_CRT_LINKAGE dynamic)
set(VCPKG_LIBRARY_LINKAGE static)

# ASAN
# Make sure this value matches up with https://llvm.org/docs/CMake.html "LLVM_USE_SANITIZER"
set(VCPKG_USE_SANITIZER "Address")
# If the following flags cause errors during build, you might need to manually
# ignore the PORT and check VCPKG_USE_SANITIZER
if(NOT PORT MATCHES "(llvm-*)")
  set(VCPKG_CXX_FLAGS "-fsanitize=address -fno-omit-frame-pointer -fno-optimize-sibling-calls -ffunction-sections -fdata-sections -Wl,-undefined,dynamic_lookup")
  set(VCPKG_C_FLAGS "-fsanitize=address -fno-omit-frame-pointer -fno-optimize-sibling-calls -ffunction-sections -fdata-sections -Wl,-undefined,dynamic_lookup")
  set(VCPKG_LINKER_FLAGS "-fsanitize=address -Wl,-undefined,dynamic_lookup")
endif()

set(VCPKG_CMAKE_SYSTEM_NAME Darwin)
set(VCPKG_OSX_ARCHITECTURES arm64)
