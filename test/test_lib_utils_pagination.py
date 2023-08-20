import unittest
from typing import List, Any
from lib.utils.pagination import create_pagination, paginate_list, WithPagination


class TestCreatePagination(unittest.TestCase):
    def test_throw_invalid_start(self):
        """
        It should throw if start is not a positive integer.
        """

        with self.assertRaises(ValueError):
            create_pagination(-1, 100, 25)

    def test_throw_invalid_total(self):
        """
        It should throw if total is not a positive integer.
        """

        with self.assertRaises(ValueError):
            create_pagination(0, -1, 25)

    def test_throw_invalid_step(self):
        """
        It should throw if step is not a non-zero positive integer.
        """

        with self.assertRaises(ValueError):
            create_pagination(0, 100, -1)

        with self.assertRaises(ValueError):
            create_pagination(0, 100, 0)

    def test_throw_start_less_total(self):
        """
        It should throw if start is not lesser than total.
        """

        with self.assertRaises(ValueError):
            create_pagination(10, 10, 5)

        with self.assertRaises(ValueError):
            create_pagination(11, 10, 5)

    def test_return_correct_total_pages(self):
        """
        It should return the correct number of pages.
        """

        self.assertEqual(create_pagination(0, 100, 25).totalPages, 4)
        self.assertEqual(create_pagination(0, 100, 33).totalPages, 4)

    #--- FIRST PAGE ---#
    def test_first_page_return_current_page(self):
        """
        It should return currentPage as 1.
        """

        self.assertEqual(create_pagination(0, 100, 25).currentPage, 1)
        self.assertEqual(create_pagination(15, 100, 25).currentPage, 1)

    def test_first_page_return_previous_start(self):
        """
        It should return previousStart as 0.
        """

        self.assertEqual(create_pagination(0, 100, 25).previousStart, 0)
        self.assertEqual(create_pagination(15, 100, 25).previousStart, 0)

    def test_first_page_return_next_start(self):
        """
        It should return the correct number for nextStart.
        """

        self.assertEqual(create_pagination(0, 100, 25).nextStart, 25)
        self.assertEqual(create_pagination(25, 100, 25).nextStart, 50)

    def test_first_page_return_is_first_page(self):
        """
        It should return firstPage as true.
        """

        self.assertTrue(create_pagination(0, 100, 25).isFirstPage)
        self.assertTrue(create_pagination(15, 100, 25).isFirstPage)

    def test_first_page_return_is_last_page(self):
        """
        It should return lastPage as false.
        """

        self.assertFalse(create_pagination(0, 100, 25).isLastPage)
        self.assertFalse(create_pagination(15, 100, 25).isLastPage)

    #--- MIDDLE PAGE ---#
    def test_middle_page_return_current_page(self):
        """
        It should return the correct number for currentPage.
        """

        self.assertEqual(create_pagination(25, 100, 25).currentPage, 2)
        self.assertEqual(create_pagination(50, 100, 25).currentPage, 3)
        self.assertEqual(create_pagination(33, 100, 33).currentPage, 2)

    def test_middle_page_return_previous_start(self):
        """
        It should return the correct number for previousStart.
        """

        self.assertEqual(create_pagination(50, 100, 25).previousStart, 25)
        self.assertEqual(create_pagination(75, 100, 25).previousStart, 50)
        self.assertEqual(create_pagination(66, 100, 33).previousStart, 33)

    def test_middle_page_return_next_start(self):
        """
        It should return the correct number for nextStart.
        """

        self.assertEqual(create_pagination(25, 100, 25).nextStart, 50)
        self.assertEqual(create_pagination(50, 100, 25).nextStart, 75)
        self.assertEqual(create_pagination(66, 100, 33).nextStart, 99)

    def test_middle_page_return_is_first_page(self):
        """
        It should return firstPage as false.
        """

        self.assertFalse(create_pagination(25, 100, 25).isFirstPage)
        self.assertFalse(create_pagination(33, 100, 33).isFirstPage)

    def test_middle_page_return_is_last_page(self):
        """
        It should return lastPage as false.
        """

        self.assertFalse(create_pagination(25, 100, 25).isLastPage)
        self.assertFalse(create_pagination(33, 100, 33).isLastPage)

    #--- LAST PAGE ---#
    def test_last_page_return_current_page(self):
        """
        It should return the correct number for currentPage.
        """

        self.assertEqual(create_pagination(75, 100, 25).currentPage, 4)
        self.assertEqual(create_pagination(99, 100, 33).currentPage, 4)

    def test_last_page_return_previous_start(self):
        """
        It should return the correct number for previousStart.
        """

        self.assertEqual(create_pagination(75, 100, 25).previousStart, 50)
        self.assertEqual(create_pagination(99, 100, 33).previousStart, 66)

    def test_last_page_return_next_start(self):
        """
        It should return the correct number for nextStart.
        """

        self.assertEqual(create_pagination(75, 100, 25).nextStart, 75)
        self.assertEqual(create_pagination(88, 100, 25).nextStart, 75)
        self.assertEqual(create_pagination(99, 100, 33).nextStart, 99)

    def test_last_page_return_is_first_page(self):
        """
        It should return firstPage as false.
        """

        self.assertFalse(create_pagination(75, 100, 25).isFirstPage)
        self.assertFalse(create_pagination(99, 100, 33).isFirstPage)

    def test_last_page_return_is_last_page(self):
        """
        It should return lastPage as true.
        """

        self.assertTrue(create_pagination(75, 100, 25).isLastPage)
        self.assertTrue(create_pagination(99, 100, 33).isLastPage)

    #--- TOTAL == 0 ---#
    def test_total_zero_return_current_page(self):
        """
        It should return the correct number for currentPage.
        """

        self.assertEqual(create_pagination(10, 0, 25).currentPage, 1)
        self.assertEqual(create_pagination(50, 0, 33).currentPage, 1)

    def test_total_zero_return_previous_start(self):
        """
        It should return the correct number for previousStart.
        """

        self.assertEqual(create_pagination(75, 0, 25).previousStart, 0)

    def test_total_zero_return_next_start(self):
        """
        It should return the correct number for nextStart.
        """

        self.assertEqual(create_pagination(75, 0, 25).nextStart, 0)

    def test_total_zero_return_is_first_page(self):
        """
        It should return firstPage as false.
        """

        self.assertTrue(create_pagination(75, 0, 25).isFirstPage)

    def test_total_zero_return_is_last_page(self):
        """
        It should return lastPage as true.
        """

        self.assertTrue(create_pagination(75, 0, 25).isLastPage)


class TestPaginateList(unittest.TestCase):
    test_list = list(range(100))

    @staticmethod
    def generate_paginated_lists(list_to_paginate: List[Any], step: int) -> List[WithPagination[List[Any]]]:
        total_pages = create_pagination(0, len(list_to_paginate), step).totalPages
        return [paginate_list(list_to_paginate, page, step) for page in range(1, total_pages + 1)]

    @staticmethod
    def expand_paginated_list(paginated_list: List[WithPagination[List[Any]]]) -> List[Any]:
        return [item for sub_list in paginated_list for item in sub_list.data]

    def test_generate_full_array_with_step_25(self):
        """
        It should generate the full array with a step of 25.
        """

        paginated_lists = TestPaginateList.generate_paginated_lists(self.test_list, 25)
        expanded_list = TestPaginateList.expand_paginated_list(paginated_lists)

        self.assertListEqual(expanded_list, self.test_list)

    def test_generate_full_array_with_step_33(self):
        """
        It should generate the full array with a step of 33.
        """

        paginated_lists = TestPaginateList.generate_paginated_lists(self.test_list, 33)
        expanded_list = TestPaginateList.expand_paginated_list(paginated_lists)

        self.assertListEqual(expanded_list, self.test_list)


if __name__ == '__main__':
    unittest.main()
