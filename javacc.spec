#
#
# Conditional build:
%bcond_with	bootstrap		# bootstrap build

Summary:	A parser/scanner generator for Java
Summary(pl.UTF-8):	Generator analizatorów/skanerów dla Javy
Name:		javacc
Version:	5.0
Release:	0.1
License:	BSD
Group:		Development/Languages/Java
Source0:	http://java.net/projects/javacc/downloads/download/%{name}-%{version}src.tar.gz
# Source0-md5:	871d78a2a5859c2eebc712c1f8135be5
Source1:	%{name}
Source2:	jjdoc
Source3:	jjtree
Patch0:		build.xml.patch
URL:		https://javacc.dev.java.net/
BuildRequires:	/bin/bash
BuildRequires:	ant
BuildRequires:	glibc-localedb-all
BuildRequires:	java-junit >= 3.8.1
BuildRequires:	jpackage-utils
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils >= 0:1.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Java Compiler Compiler (JavaCC) is the most popular parser generator
for use with Java applications. A parser generator is a tool that
reads a grammar specification and converts it to a Java program that
can recognize matches to the grammar. In addition to the parser
generator itself, JavaCC provides other standard capabilities related
to parser generation such as tree building (via a tool called JJTree
included with JavaCC), actions, debugging, etc.

%description -l pl.UTF-8
Java Compiler Compiler (JavaCC) to najbardziej popularny generator
analizatorów do używania w aplikacjach Javy. Generator analizatorów to
narzędzie czytające specyfikację gramatyki i przekształcające ją na
program w Javie rozpoznający dopasowania do gramatyki. Oprócz samego
generatora analizatorów JavaCC udostępnia inne standardowe możliwości
związane z generowaniem analizatorów, takie jak budowanie drzewa
(poprzez narzędzie o nazwie JJTree dołączone do JavaCC), akcje,
diagnostykę itp.

%package manual
Summary:	Manual for JavaCC
Summary(pl.UTF-8):	Podręcznik do JavaCC
Group:		Documentation

%description manual
Manual for JavaCC.

%description manual -l pl.UTF-8
Podręcznik do JavaCC.

%package demo
Summary:	Examples for JavaCC
Summary(pl.UTF-8):	Przykłady do JavaCC
Group:		Documentation

%description demo
Examples for JavaCC.

%description demo -l pl.UTF-8
Przykłady do JavaCC.

%prep
%setup -qc
mv %{name}/* .; rmdir %{name}
%patch0 -p1

cp -p %{SOURCE1} javacc
cp -p %{SOURCE2} jjdoc
cp -p %{SOURCE3} jjtree

# Remove binary information in the source tar
rm lib/junit3.8.1/junit.jar
%if %{without bootstrap}
rm bootstrap/javacc.jar
%endif

find examples -type f | xargs %undos

sed -i -e 's/source="1.4"/source="1.5"/g' src/org/javacc/{parser,jjdoc,jjtree}/build.xml

mv www/doc .

%build
%if %{without bootstrap}
# Use the bootstrap javacc.jar to generate some required
# source java files. After these source files are generated we
# remove the bootstrap jar and build the binary from source.
jar=$(find-jar javacc)
ln -sf $jar bootstrap/javacc.jar
%endif

%ant -f src/org/javacc/parser/build.xml parser-files
%ant -f src/org/javacc/jjtree/build.xml tree-files

required_jars="junit"
export CLASSPATH=$(build-classpath $required_jars)

%ant \
	jar

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p bin/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

install -d $RPM_BUILD_ROOT%{_bindir}
install -p javacc jjdoc jjtree $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README
%attr(755,root,root) %{_bindir}/javacc
%attr(755,root,root) %{_bindir}/jjdoc
%attr(755,root,root) %{_bindir}/jjtree
%{_javadir}/javacc-%{version}.jar
%{_javadir}/javacc.jar

%files manual
%defattr(644,root,root,755)
%doc doc/*

%files demo
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
