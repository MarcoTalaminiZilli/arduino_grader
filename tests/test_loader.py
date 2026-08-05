from core.loader import CodeLoader

def test_remove_comments():
    codigo_com_comentario = """
    void setup() {
        // Inicializa o pino
        pinMode(13, OUTPUT); 
    }
    /* 
       Bloco de comentario
       multiplas linhas
    */
    void loop() {}
    """
    
    codigo_limpo = CodeLoader.remove_comments(codigo_com_comentario)
    
    # Verifica se os comentários sumiram, mas as funções continuam
    assert "// Inicializa o pino" not in codigo_limpo
    assert "Bloco de comentario" not in codigo_limpo
    assert "pinMode(13, OUTPUT);" in codigo_limpo
    assert "void setup()" in codigo_limpo