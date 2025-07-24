#pragma once
#ifndef DOCTEST_VERSION_MAJOR
// Fallback minimal stub – only for static analysis; real doctest will override.
#include <exception>
#include <iostream>
namespace doctest {
struct TestFailureException : public std::exception { const char* what() const noexcept override { return "doctest::fail"; } };
inline void fail(const char* msg) { std::cerr << msg << std::endl; throw TestFailureException(); }
}
#define TEST_CASE(name) static void name(); static int _autorun_##name = ([](){ name(); return 0; })(); static void name()
#define CHECK(expr) do { if(!(expr)) doctest::fail("CHECK failed"); } while(0)
#define CHECK_FALSE(expr) CHECK(!(expr))
#define CHECK_NOTHROW(expr) do { try { expr; } catch(...) { doctest::fail("Unexpected throw"); } } while(0)
#endif 