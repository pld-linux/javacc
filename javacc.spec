Summary:	A parser/scanner generator for Java
Summary(pl.UTF-8):	Generator analizatorów/skanerów dla Javy
Name:		javacc
Version:	4.0
Release:	1
License:	BSD
Source0:	https://javacc.dev.java.net/files/documents/17/26783/%{name}-%{version}src.tar.gz
# Source0-md5:	bf91835dc1bb4821f4b26fd552b43c8d
Source1:	%{name}
Source2:	jjdoc
Source3:	jjtree
Group:		Development/Languages/Java
URL:		https://javacc.dev.java.net/
BuildRequires:	/bin/bash
BuildRequires:	ant
BuildRequires:	jpackage-utils
BuildRequires:	junit >= 3.8.1
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
%setup -q -n %{name}
cp %{SOURCE1} javacc
cp %{SOURCE2} jjdoc
cp %{SOURCE3} jjtree
mv www/doc .

%build
required_jars="junit"
export CLASSPATH=$(/usr/bin/build-classpath $required_jars)

%ant \
	-Dversion=%{version} \
	jar

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
install bin/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
install -d $RPM_BUILD_ROOT%{_bindir}
install javacc jjdoc jjtree $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr examples $RPM_BUILD_ROOT%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README
%attr(755,root,root) %{_bindir}/*
%{_javadir}/*.jar

%files manual
%defattr(644,root,root,755)
%doc doc/*

%files demo
%defattr(644,root,root,755)
%{_datadir}/%{name}
