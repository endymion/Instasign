#include <iostream>
#include <time.h>
#include <string.h>

long parseISO8601(const char* time_str) {
    struct tm tm;
    memset(&tm, 0, sizeof(tm));
    if (strptime(time_str, "%Y-%m-%dT%H:%M:%SZ", &tm) != NULL) {
        return timegm(&tm);
    }
    return 0;
}

int main() {
    std::cout << parseISO8601("2026-07-21T17:15:00Z") << std::endl;
    return 0;
}
