#include<bits/stdc++.h>
#include<math.h>

using namespace std;

int main()
{
    int n;
    cin>>n;
    float res=0;
    for(int i=1;i<=n;i++)
    {
        res+=(i/(pow(i+2,i+1)));
    }
    cout<<res<<endl;
    return 0;
}