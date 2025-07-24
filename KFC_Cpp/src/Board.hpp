#pragma once

#include "img.hpp"
#include <utility>

// ---------------------------------------------------------------------------
// Board – C++ translation of KungFu Chess Python Board dataclass
// ---------------------------------------------------------------------------
// Responsible only for coordinate conversions and image holder. Pixel drawing
// is delegated to Img.  The API mirrors the original Python version so that the
// unit-tests can be translated with minimal changes.
// ---------------------------------------------------------------------------

class Board {
public:
    // ---------------------------------------------------------------------
    // Constructors
    // ---------------------------------------------------------------------
    Board(int cell_H_pix,
          int cell_W_pix,
          int W_cells,
          int H_cells,
          const Img& image,
          float cell_H_m = 1.0f,
          float cell_W_m = 1.0f);

    // Defaulted special members – value semantics are fine (cv::Mat uses ref-count)
    Board(const Board&) = default;
    Board(Board&&) noexcept = default;
    Board& operator=(const Board&) = default;
    Board& operator=(Board&&) noexcept = default;
    ~Board() = default;

    // ---------------------------------------------------------------------
    // Behaviour identical to Python version
    // ---------------------------------------------------------------------
    Board clone() const;                 // Deep-copy of image holder
    void show() const;                   // Show only if an image is loaded

    // Coordinate conversions -------------------------------------------------
    std::pair<int, int> m_to_cell(const std::pair<float, float>& pos_m) const;
    std::pair<float, float> cell_to_m(const std::pair<int, int>& cell) const;
    std::pair<int, int> m_to_pix(const std::pair<float, float>& pos_m) const;

    // ---------------------------------------------------------------------
    // Public data – kept for 1-to-1 mapping with Python dataclass.  This makes
    // porting code simpler, but if stronger encapsulation is desired these can
    // be turned into private with accessors.
    // ---------------------------------------------------------------------
    int cell_H_pix;
    int cell_W_pix;
    int W_cells;
    int H_cells;

    Img img;              // board image
    float cell_H_m;
    float cell_W_m;
}; 