using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SimpleShader : MonoBehaviour
{
    public Material material;

    public float timer;

    // Update is called once per frame
    void Update()
    {
        timer += Time.deltaTime;

        material.SetFloat("_time", timer);
    }
}
