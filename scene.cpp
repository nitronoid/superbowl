#include <ri.h>
#include <array>
#include <vector>
#include <string>

#define RI (char*)

template <typename R, typename T, typename F>
std::vector<R> conv(std::vector<T>& source, F lambda)
{
    std::vector<R> target(source.size());
    std::transform(source.begin(), source.end(), target.begin(), lambda);
    return target;
}

int main(int argc, char *argv[])
{
    RiBegin(RI_NULL);

    // Define and cast all search paths
    std::vector<const char*> tokens{"archive", "shader", "texture"};
    std::vector<const char*> parms{".", "./shaders", "./textures"};
    RiOptionV(RI"searchpath", tokens.size(), 
        &conv<RtToken>(tokens, [](const char * c) { return const_cast<char*>(c); })[0],
        &conv<RtPointer>(parms,[](const char * &c) { return static_cast<RtPointer>(&c);})[0]);

    RiDisplay(RI"scene.tiff",RI"file",RI"rgba",RI_NULL);
    float fov = 50.f;
    RiProjection(RI"perspective", RI"fov", &fov, RI_NULL);

    RiTranslate(0,0,10);
    RiWorldBegin();
        RiAttributeBegin();
            std::vector<const char*> pTokens{"_colU", "_colV"};
            std::vector<RtColor> pParms{RtColor{0.1,0.9,0.1},RtColor{0.9,0.1,0.1}};
            RiPattern(RI"",RI"test", pTokens.size(),
                &conv<RtToken>(pTokens, [](const char * c) { return const_cast<char*>(c); })[0],
                &pParms[0]
                );
            RiReadArchive(RI"owl.rib", 0, RI_NULL);
        RiAttributeEnd();
    RiWorldEnd();

    RiEnd();
    return 0;
}