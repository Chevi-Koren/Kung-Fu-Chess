#pragma once

#include "Graphics.hpp"
#include <memory>
#include <string>
#include <optional>

namespace nlohmann { class json; }

// Simple GraphicsFactory that forwards an image loader placeholder to
// Graphics.  In this head-less C++ port, the img_loader is unused but the
// factory mirrors the Python API expected by the unit tests.
class GraphicsFactory {
public:
    // The Python version receives an img_loader which is stored and passed to
    // Graphics objects.  Here we accept any pointer (void*) just to satisfy the
    // signature – the loader does nothing inside our stubbed Graphics.
    explicit GraphicsFactory(void* /*img_loader*/ = nullptr) {}

    std::shared_ptr<Graphics> load(const std::string& sprites_dir,
                                   const nlohmann::json& /*cfg*/, // ignored for now
                                   std::pair<int,int> cell_size) const {
        // Simply create Graphics with the provided path and size.
        return std::make_shared<Graphics>(sprites_dir, cell_size);
    }
}; 