#!/usr/bin/env python2

import argparse
import sys
import os
import platform

from installers import utils, common, windows

target_list = ["xed", "llvm", "gflags", "gtest", "protobuf", "glog", "capstone", "cmake"]

template_list = dict()
template_list["mcsema2"] = set()
template_list["mcsema2"].add("llvm")
template_list["mcsema2"].add("xed")
template_list["mcsema2"].add("gtest")
template_list["mcsema2"].add("glog")
template_list["mcsema2"].add("gflags")
template_list["mcsema2"].add("protobuf")
template_list["mcsema2"].add("capstone")
template_list["mcsema2"].add("cmake")

def main():
  # parse the command line
  arg_parser = argparse.ArgumentParser(description="This utility is used to build common libraries for various Trail of Bits products.")
  arg_parser.add_argument("--llvm_version", type=int, help="LLVM version, specified as a single integer (i.e.: 38, 39, 40, ...)", default=40)
  arg_parser.add_argument("--repository_path", type=str, help="This is where the repository is installed", default="/opt/trailofbits/libraries")

  target_group = arg_parser.add_mutually_exclusive_group(required=True)

  target_list_description = "The targets to build, separated by commas. Available targets: " + str(target_list)
  target_group.add_argument("--targets", type=str, help=target_list_description)

  template_list_description = "The template to build. Available templates: " + str(template_list.keys())
  target_group.add_argument("--template", type=str, help=template_list_description)

  args = arg_parser.parse_args()

  # acquire the targets
  if args.template is not None:
    if args.template not in template_list:
      print("Invalid template name: " + args.template)
      return False

    targets_to_install = template_list[args.template]

  else:
    targets_to_install = args.targets.split(",")

  # validate the targets
  for target in targets_to_install:
    if target not in target_list:
      print("Invalid target: " + target)
      return False

  # get the llvm version
  llvm_version = str(args.llvm_version)
  if len(llvm_version) != 2:
    print("Invalid LLVM version: " + str(llvm_version))
    return False

  properties = dict()
  properties["llvm_version"] = llvm_version
  properties["repository_path"] = args.repository_path

  # print a summary of what we are about to do
  print("Repository path: " + args.repository_path)

  print("LLVM version: " + llvm_version),
  if args.llvm_version < 36 or args.llvm_version >= 50:
    print("(unsupported)")
  else:
    print("(supported)")

  print("Target list: " + str(targets_to_install) + "\n")

  # build each target
  if not os.path.exists("sources"):
    os.makedirs("sources")

  if not os.path.exists("temp"):
    os.makedirs("temp")

  if not os.path.exists("build"):
    os.makedirs("build")

  for target in targets_to_install:
    print(target)

    package_installer = get_package_installer(target)
    if package_installer is None:
      print(" x The package installer procedure is missing")
      continue

    package_installer(properties)

  return True

def get_package_installer(package_name):
  """
  Returns the specified package installer
  """

  system_name = get_system_name()
  if system_name == None:
    return None

  function_name = system_name + "_installer_" + package_name
  function = get_function(function_name)
  if function is not None:
    return function

  function_name = "common_installer_" + package_name
  function = get_function(function_name)
  if function is not None:
    return function

  return None

def get_function(function_name):
  """
  Returns the specified function
  """

  module_list = globals().copy()
  module_list.update(locals())

  function = None
  for module_name in module_list:
      try:
          function = getattr(module_list[module_name], function_name)
          if function is not None:
              break

      except Exception:
          pass

  return function

def get_system_name():
  """
  Returns the system name (windows, macos, linux-distroname)
  """

  name = get_platform_type()
  if name == None:
    return None

  if name == "linux":
    distribution_name = get_linux_distribution_name()
    if distribution_name == None:
      return None

    name = name + "-" + distribution_name

  return name

def get_linux_distribution_name():
  """
  Returns the distribution name.
  """

  distribution_info = platform.linux_distribution(
                      supported_dists=platform._supported_dists + ('arch',))

  name = distribution_info[0]
  if not name:
    return None

  return name

def get_platform_type():
  """
  Returns the platform type (linux, windows, macos or None in case of error)
  """

  if sys.platform == "linux" or sys.platform == "linux2":
    return "linux"

  elif sys.platform == "darwin":
    return "macos"

  elif sys.platform == "win32" or sys.platform == "cygwin":
    return "windows"

  else:
    return None

  name = distribution_info[0]
  if not name:
    return None

  return name

if __name__ == "__main__":
  if not main():
    sys.exit(1)

  sys.exit(0)
