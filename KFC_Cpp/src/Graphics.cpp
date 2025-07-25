#include "Graphics.hpp"

#include <algorithm>
#include <chrono>
#include <stdexcept>

Graphics::Graphics(const std::string& sprites_folder,
                   std::pair<int,int> cell_size,
                   bool loop_, double fps_)
    : loop(loop_), fps(fps_), frame_duration_ms(1000.0 / fps_) {
    // very simplified: load no real sprites; just push one blank image
    Img blank;
#if KFC_HAVE_OPENCV
    cv::Mat mat(cell_size.second, cell_size.first, CV_8UC4, cv::Scalar(0,0,0,0));
#else
    cv::Mat mat;
    mat.rows = cell_size.second;
    mat.cols = cell_size.first;
#endif
    blank.set_mat(mat);
    frames.push_back(blank);
}

void Graphics::reset(const Command& cmd) {
    start_ms = cmd.timestamp;
    cur_frame = 0;
}

void Graphics::update(int now_ms) {
    int elapsed = now_ms - start_ms;
    int frames_passed = static_cast<int>(elapsed / frame_duration_ms);
    if(loop)
        cur_frame = frames_passed % frames.size();
    else
        cur_frame = std::min<size_t>(frames_passed, frames.size()-1);
}

const Img& Graphics::get_img() const {
    if(frames.empty()) throw std::runtime_error("Graphics has no frames loaded");
    return frames[cur_frame];
} 