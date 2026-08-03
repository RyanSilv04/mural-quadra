-- Cria o banco de dados do mural
CREATE DATABASE IF NOT EXISTS mural_quadra;
USE mural_quadra;

-- Tabela que guarda os avisos/eventos da quadra
CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    conteudo TEXT NOT NULL,
    data_evento DATE,              -- data do evento (opcional, ex: reserva da quadra)
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alguns dados de exemplo para você já ver o mural funcionando
INSERT INTO posts (titulo, conteudo, data_evento) VALUES
('Quadra interditada para manutenção', 'A quadra ficará fechada para pintura da linha demarcatória.', '2026-08-02'),
('Torneio de vôlei', 'Inscrições abertas na secretaria até sexta-feira.', '2026-08-15');
