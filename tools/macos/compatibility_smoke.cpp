#include <cassert>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include "Ply.h"
#include "SparseMatrix.h"
int main() {
    Point3D<double> p, q, n;
    for (int i=0;i<3;i++) { p[i]=i+4; q[i]=i+1; n[i]=i+2; }
    PlyOrientedVertex<double> a(p,n), b(q,n);
    auto c=a-b;
    for (int i=0;i<3;i++) { assert(c.point[i]==3); assert(c.normal[i]==0); }
    PlyColorVertex<double>::_PlyColorVertex x(p,p), y(q,q);
    auto z=x-y;
    for (int i=0;i<3;i++) { assert(z.point[i]==3); assert(z.color[i]==3); }
    SparseMatrix<double> matrix;
    matrix.Resize(3); matrix.SetRowSize(1,1);
    matrix[1][0]=MatrixEntry<double>(1,7);
    matrix.SetZero();
    assert(matrix.rows==3);
    for (int i=0;i<3;i++) assert(matrix.rowSizes[i]==0);
}
