from deal_all_infor.scanf_all import scanTask
# from tests import tests
if  __name__  ==  "__main__":
    """
    测试
    """
    test_func = scanTask('10.10.9.252-10.10.9.252', 6000, 7000, ["redis"])
    # test_func.scanf_part()
    test_func.run()
    print("over")