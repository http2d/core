/*
 * test1.cpp
 *
 *  Created on: Jun 15, 2013
 *      Author: alo
 */

#include "gtest/gtest.h"
#include "boost/locale.hpp"

namespace loc = boost::locale;

TEST(BoostUTF8, Basics) {
	std::string UTF8String = u8"çlvaro L—pez Ortega";
	EXPECT_EQ (UTF8String.size(),   19);
	EXPECT_EQ (UTF8String.length(), 19);
}

TEST(BoostUTF8, LetterPosition) {
	std::string UTF8String = u8"ca–—n";
	EXPECT_EQ(UTF8String[3], '—');
	EXPECT_EQ(UTF8String[4], 'n');
}

int
main (int argc, char **argv)
{
	::testing::InitGoogleTest(&argc, argv);
	return RUN_ALL_TESTS();
}
