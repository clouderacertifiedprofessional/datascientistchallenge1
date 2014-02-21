datascientistchallenge1
=======================

This project contains all of the code used in the CCP: Data Scientist Challenge One Solution Kit.
These scripts and applications require the solution kit data to be useful.  You can find the
solution kit data preloaded on the solution kit virtual machine.

To make use of there scripts, copy the target script into your working directory as the desired
name.  In the cases where the solution kit suggests editing an existing file, you can find the
file that results from the edit here with "_editN" appended to the name, where "N" is a
number indicating which round of modifications produces the resulting file.

For the recommendation problem, rather than having multiple versions of the Java source files
in the source directory, the entire Maven project has been cloned and marked with "_editN".
The reason is that the Maven project will not build if there are broken source files in the
project.  If a class named X is in a file named X_edit1.java, that source file will not
compile, hence breaking the build.  By including full copies of the project, each of the
projects is able to be built.  When using the files from the Maven projects, you don't need
to copy over the entire Maven project is you'd prefer not to.  You can instead simply copy
the files that you want into an existing project.

