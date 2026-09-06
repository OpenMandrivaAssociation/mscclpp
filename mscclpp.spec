# MSCCL++ GPU-driven collectives. v0.10.0.

Name:		mscclpp
Version:	0.10.0
Release:	1
Summary:	GPU-driven communication stack (MSCCL++)
License:	MIT
Group:		System/Libraries
URL:		https://github.com/microsoft/mscclpp
Source0:	https://github.com/microsoft/mscclpp/archive/refs/tags/v%{version}.tar.gz#/mscclpp-%{version}.tar.gz

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	hipcc
BuildRequires:	rocm-hip-devel
BuildRequires:	pkgconfig(libibverbs)
BuildRequires:	clang >= %{rocm_llvm_maj_ver}

%description
MSCCL++ is a GPU-driven communication library used as an optional
faster path inside RCCL (-DENABLE_MSCCLPP).

%package devel
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and CMake package for MSCCL++.

%prep
%autosetup -n mscclpp-%{version} -p1

%build
export CXX=hipcc
export CC=clang
%cmake %{rocm_cmake_fhs} %{rocm_cmake_gpu_targets_rccl} \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_CXX_COMPILER=hipcc \
	-DMSCCLPP_USE_ROCM=ON \
	-DMSCCLPP_USE_CUDA=OFF \
	-DMSCCLPP_BUILD_TESTS=OFF \
	-DMSCCLPP_BUILD_PYTHON_BINDINGS=OFF \
	-DMSCCLPP_USE_GDRCOPY=OFF \
	-DMSCCLPP_BYPASS_GPU_CHECK=ON \
	-DROCM_PATH=%{_prefix} \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

%files
%license LICENSE
%doc README.md
%{_libdir}/libmscclpp.so.*

%files devel
%{_includedir}/mscclpp/
%{_libdir}/libmscclpp.so
%{_libdir}/cmake/mscclpp/
