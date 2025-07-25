#pragma once

#include <unordered_map>
#include <string>
#include <initializer_list>

namespace nlohmann {
class json {
    std::unordered_map<std::string, double> data;
public:
    json() = default;
    json(std::initializer_list<std::pair<const std::string, double>> init) {
        for (const auto& kv : init) data[kv.first] = kv.second;
    }

    double value(const std::string& key, double default_val) const {
        auto it = data.find(key);
        return it != data.end() ? it->second : default_val;
    }

    double& operator[](const std::string& key) { return data[key]; }
    const double& operator[](const std::string& key) const { return data.at(key); }

    bool contains(const std::string& key) const { return data.find(key) != data.end(); }
};
} 