from core.evaluator import CodeEvaluator

def test_check_essential_structures():
    # Simulando um código correto
    codigo_valido = "void setup() {} void loop() {}"
    resultado = CodeEvaluator.check_essential_structures(codigo_valido)
    assert resultado["has_setup"] == True
    assert resultado["has_loop"] == True

    # Simulando um código faltando o setup
    codigo_invalido = "void loop() {}"
    resultado = CodeEvaluator.check_essential_structures(codigo_invalido)
    assert resultado["has_setup"] == False
    assert resultado["has_loop"] == True

def test_extract_function_calls():
    codigo = "void setup() { pinMode(13, OUTPUT); Serial.begin(9600); }"
    chamadas = CodeEvaluator.extract_function_calls(codigo)
    
    # Verifica se extraiu as funções corretas e ignorou o 'setup'
    assert "pinMode" in chamadas
    assert "Serial" in chamadas # No regex atual, ele pega 'Serial' antes do ponto
    assert "setup" not in chamadas

def test_evaluate_score():
    # Testando o cálculo final da nota
    solucao = "void setup() { pinMode(13, OUTPUT); } void loop() { digitalWrite(13, HIGH); }"
    aluno = "void setup() { pinMode(13, OUTPUT); } void loop() {}" # Faltou o digitalWrite
    
    pesos = {"estrutura_basica": 50.0, "chamadas_funcao": 50.0}
    
    resultado = CodeEvaluator.evaluate(solucao, aluno, pesos)
    
    # O aluno tem setup/loop (50 pts), mas só acertou metade das chamadas (25 pts)
    assert resultado["final_score"] == 75.0