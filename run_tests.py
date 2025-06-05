import unittest

if __name__ == '__main__':
    # Descobre e executa todos os testes
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Retorna código de saída apropriado para sistemas CI/CD
    exit(not result.wasSuccessful())