#pragma once

#include "img.hpp"
#include "Command.hpp"
#include <vector>
#include <string>

class Graphics {
public:
    Graphics(const std::string& sprites_folder,
             std::pair<int,int> cell_size,
             bool loop = true,
             double fps = 6.0);

    void reset(const Command& cmd);
    void update(int now_ms);
    const Img& get_img() const;

private:
    std::vector<Img> frames;
    bool loop{true};
    double fps{6.0};
    int start_ms{0};
    size_t cur_frame{0};
    double frame_duration_ms{0};
}; 