from conans import ConanFile, CMake, tools
import os


class ExampleConan(ConanFile):
    name = "example"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake",

    def requirements(self):
        self.requires("asio/1.24.0")
        self.requires("fmt/9.1.1")
        self.requires("hello/2.0.1@world/stable")

    def imports(self):
        if self.options.example:
            self.copy("*.so*", dst="./bin", src="lib")
            self.copy("*.dll", dst="./bin", src="bin")

    def build(self):
        cmake = CMake(self, parallel=True)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self, parallel=True)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["example"]
