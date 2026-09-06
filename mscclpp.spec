# MSCCL++ GPU-driven collectives. v0.10.0.

Name:		mscclpp
Version:	0.10.0
Release:	1
Summary:	GPU-driven communication stack (MSCCL++)
License:	MIT
Group:		System/Libraries
URL:		https://github.com/microsoft/mscclpp
Source0:	https://github.com/microsoft/mscclpp/archive/refs/tags/v%{version}.tar.gz#/mscclpp-%{version}.tar.gz
Patch0:		0001-system-nlohmann-json.patch
Patch1:		0002-nccl-cstring.patch

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	hipcc
BuildRequires:	rocm-hip-devel
BuildRequires:	pkgconfig(libibverbs)
BuildRequires:	cmake(nlohmann_json)
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
CXXFLAGS=$(printf '%s' "%{optflags}" | sed 's/-mfpmath=sse//g')
export CXXFLAGS
%cmake %{rocm_cmake_fhs} \
	-DAMDGPU_TARGETS="gfx1100;gfx1101;gfx1200;gfx1201" \
	-DGPU_TARGETS="gfx1100;gfx1101;gfx1200;gfx1201" \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_CXX_COMPILER=hipcc \
	-DCMAKE_HIP_COMPILER=clang++ \
	-DCMAKE_HIP_ARCHITECTURES="gfx1100;gfx1101;gfx1200;gfx1201" \
	-DCMAKE_CXX_FLAGS="$CXXFLAGS" \
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
if [ -d %{buildroot}/usr/lib ]; then
	mkdir -p %{buildroot}%{_libdir}
	mv %{buildroot}/usr/lib/libmscclpp*.so* %{buildroot}%{_libdir}/ 2>/dev/null || true
	rm -f %{buildroot}/usr/lib/libmscclpp_static.a
	rmdir %{buildroot}/usr/lib 2>/dev/null || true
fi
rm -f %{buildroot}%{_includedir}/mscclpp/version.hpp.in

%files
%license LICENSE
%doc README.md
%{_libdir}/libmscclpp.so.*
%{_libdir}/libmscclpp_collectives.so.*
%{_libdir}/libmscclpp_nccl.so.*
%{_libdir}/libmscclpp_audit_nccl.so.*

%files devel
%{_includedir}/mscclpp/
%{_libdir}/libmscclpp.so
%{_libdir}/libmscclpp_collectives.so
%{_libdir}/libmscclpp_nccl.so
%{_libdir}/libmscclpp_audit_nccl.so
