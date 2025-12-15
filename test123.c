#include <stdio.h>
#include <ctype.h>
#include <string.h>

#define MAX_SYMBOLS 100
#define MAX_SOURCE 10000

typedef struct {
    char name[50];
    char type[10];
    int size;
    int address;
    int value;
} Symbol;

Symbol symbolTable[MAX_SYMBOLS];
int symbolCount = 0;

/* ---------------- SYMBOL TABLE ---------------- */

void addSymbol(char* name, char* type, int size, int address, int value) {
    for (int i = 0; i < symbolCount; i++) {
        if (strcmp(symbolTable[i].name, name) == 0)
            return; // avoid duplicate
    }

    if (symbolCount < MAX_SYMBOLS) {
        strcpy(symbolTable[symbolCount].name, name);
        strcpy(symbolTable[symbolCount].type, type);
        symbolTable[symbolCount].size = size;
        symbolTable[symbolCount].address = address;
        symbolTable[symbolCount].value = value;
        symbolCount++;
    }
}

void printSymbolTable() {
    printf("\n===== SYMBOL TABLE =====\n");
    printf("Name\tType\tSize\tAddress\tValue\n");
    for (int i = 0; i < symbolCount; i++) {
        printf("%s\t%s\t%d\t%d\t%d\n",
               symbolTable[i].name,
               symbolTable[i].type,
               symbolTable[i].size,
               symbolTable[i].address,
               symbolTable[i].value);
    }
}

/* ---------------- TOKEN UTIL ---------------- */

void printToken(const char* token, const char* type) {
    printf("%-15s : %s\n", token, type);
}

int isKeyword(const char* str) {
    const char* keywords[] = {
        "auto","break","case","char","const","continue","default","do",
        "double","else","enum","extern","float","for","goto","if","int",
        "long","register","return","short","signed","sizeof","static",
        "struct","switch","typedef","union","unsigned","void","volatile","while"
    };

    for (int i = 0; i < 32; i++) {
        if (strcmp(str, keywords[i]) == 0)
            return 1;
    }
    return 0;
}

/* ---------------- LEXICAL ANALYZER ---------------- */

void tokenize(const char* source) {
    char buffer[100];
    int i = 0, j = 0;

    while (source[i] != '\0') {

        /* Identifier or Keyword */
        if (isalpha(source[i]) || source[i] == '_') {
            j = 0;
            while (isalnum(source[i]) || source[i] == '_') {
                buffer[j++] = source[i++];
            }
            buffer[j] = '\0';

            if (isKeyword(buffer)) {
                printToken(buffer, "KEYWORD");
            } else {
                printToken(buffer, "IDENTIFIER");
                addSymbol(buffer, "int", 4, 1000 + symbolCount * 4, 0);
            }
        }

        /* Number */
        else if (isdigit(source[i])) {
            j = 0;
            while (isdigit(source[i])) {
                buffer[j++] = source[i++];
            }
            buffer[j] = '\0';
            printToken(buffer, "INTEGER");
        }

        /* String */
        else if (source[i] == '"') {
            j = 0;
            buffer[j++] = source[i++];
            while (source[i] != '"' && source[i] != '\0') {
                buffer[j++] = source[i++];
            }
            buffer[j++] = '"';
            buffer[j] = '\0';
            i++;
            printToken(buffer, "STRING");
        }

        /* Operators */
        else if (strchr("+-*/%=<>!", source[i])) {
            buffer[0] = source[i++];
            buffer[1] = '\0';
            printToken(buffer, "OPERATOR");
        }

        /* Special characters */
        else if (strchr(";(),{}", source[i])) {
            buffer[0] = source[i++];
            buffer[1] = '\0';
            printToken(buffer, "SPECIAL CHAR");
        }

        else {
            i++;
        }
    }
}

/* ---------------- MAIN ---------------- */

int main() {
    char source[MAX_SOURCE];
    printf("=== Mini Compiler Output ===\n");

    /* Read input from stdin */
    size_t len = fread(source, 1, sizeof(source) - 1, stdin);
    source[len] = '\0';

    printf("===== TOKENS =====\n");
    tokenize(source);

    printSymbolTable();
    return 0;
}
